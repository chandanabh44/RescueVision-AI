"""
RescueVision AI - Database Models
Defines SQLAlchemy models for Incidents, Official Alerts, Data Source Metadata,
Image Analysis Logs, and Audit Events.
"""

from datetime import datetime, timezone
import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def utc_now():
    """Return timezone-aware current UTC time."""
    return datetime.now(timezone.utc)


def make_aware(dt):
    """Ensure datetime is timezone-aware UTC datetime."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class Incident(db.Model):
    """
    User-submitted disaster reports and historical/simulated incident records.
    Maintains strict separation between user reports and verified official records.
    """
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True)
    incident_uuid = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()), index=True)
    disaster_type = db.Column(db.String(50), nullable=False, index=True)  # flood, earthquake, wildfire, landslide
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location_name = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    severity = db.Column(db.String(50), nullable=False, default="Moderate")  # Low, Moderate, Severe, Critical
    
    # Status progression: Saved locally -> Submitted -> Awaiting review -> Verified by reviewer -> Rejected or resolved
    status = db.Column(db.String(50), nullable=False, default="Awaiting review", index=True)
    
    # Data Origin classification
    data_origin = db.Column(db.String(50), nullable=False, default="user_report", index=True)
    # user_report | official_feed | demo_simulation | historical_dataset

    # Reporter Details - strictly confidential; never exposed via public endpoints
    reporter_name = db.Column(db.String(100), nullable=True)
    reporter_contact = db.Column(db.String(150), nullable=True)
    
    # Uploaded image reference
    image_filename = db.Column(db.String(255), nullable=True)

    # Verification workflow
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    verification_notes = db.Column(db.Text, nullable=True)
    verified_by = db.Column(db.String(100), nullable=True)

    # Demo flag - Never mistake for a real incident
    is_demo = db.Column(db.Boolean, default=False, nullable=False, index=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def to_dict(self, is_admin: bool = False) -> dict:
        """
        Serialize incident object to dictionary.
        Hides private reporter identity from public visitors.
        """
        data = {
            "id": self.id,
            "uuid": self.incident_uuid,
            "disaster_type": self.disaster_type,
            "title": self.title,
            "description": self.description,
            "location_name": self.location_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "severity": self.severity,
            "status": self.status,
            "data_origin": self.data_origin,
            "image_filename": self.image_filename,
            "image_url": f"/uploads/{self.image_filename}" if self.image_filename else None,
            "is_verified": self.is_verified,
            "is_demo": self.is_demo,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "origin_badge": {
                "user_report": "User Report (Community)",
                "official_feed": "Official Feed",
                "demo_simulation": "DEMO DATA (Simulation)",
                "historical_dataset": "Historical Dataset Example"
            }.get(self.data_origin, "Unverified Report")
        }

        # Privacy protection: Only authorized administrators see personal contact details
        if is_admin:
            data["reporter_name"] = self.reporter_name or "Anonymous"
            data["reporter_contact"] = self.reporter_contact or "None provided"
            data["verification_notes"] = self.verification_notes
            data["verified_by"] = self.verified_by
        else:
            data["reporter_name"] = "Anonymous Community Reporter" if self.reporter_name else "Anonymous"

        return data


class OfficialAlert(db.Model):
    """
    Authoritative alerts retrieved from real-time official feeds
    (e.g., USGS Earthquake API, NASA EONET, Open-Meteo Flood/Weather).
    """
    __tablename__ = "official_alerts"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)  # USGS, NASA EONET, Open-Meteo
    source_record_id = db.Column(db.String(200), unique=True, nullable=False, index=True)
    disaster_type = db.Column(db.String(50), nullable=False, index=True)  # flood, earthquake, wildfire, landslide
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    severity = db.Column(db.String(50), nullable=False, default="Moderate")
    
    event_time = db.Column(db.DateTime, nullable=False)
    retrieved_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    
    verification_status = db.Column(db.String(50), nullable=False, default="Official Verified")
    source_url = db.Column(db.String(500), nullable=True)
    raw_metadata = db.Column(db.Text, nullable=True)  # JSON dump of provider response
    
    is_demo = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "source_record_id": self.source_record_id,
            "disaster_type": self.disaster_type,
            "title": self.title,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "severity": self.severity,
            "event_time": self.event_time.isoformat() if self.event_time else None,
            "retrieved_at": self.retrieved_at.isoformat() if self.retrieved_at else None,
            "verification_status": self.verification_status,
            "source_url": self.source_url,
            "is_demo": self.is_demo,
            "is_active": self.is_active,
            "is_stale": (utc_now() - make_aware(self.retrieved_at)).total_seconds() > 86400 if self.retrieved_at else False
        }


class DataSourceMetadata(db.Model):
    """
    Tracks health, timestamps, and status of external disaster API integrations.
    """
    __tablename__ = "data_source_metadata"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    api_endpoint = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default="Active", nullable=False)  # Active, Unavailable, Rate Limited, Demo Only
    last_checked = db.Column(db.DateTime, default=utc_now, nullable=False)
    last_success = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    record_count = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "api_endpoint": self.api_endpoint,
            "status": self.status,
            "last_checked": self.last_checked.isoformat() if self.last_checked else None,
            "last_success": self.last_success.isoformat() if self.last_success else None,
            "error_message": self.error_message,
            "record_count": self.record_count
        }


class ImageAnalysisLog(db.Model):
    """
    Stores image upload records, classification results, and mandatory limitation disclaimers.
    """
    __tablename__ = "image_analysis_logs"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size_kb = db.Column(db.Float, nullable=False)
    predicted_category = db.Column(db.String(50), nullable=False)
    confidence_score = db.Column(db.Float, nullable=True)
    model_version = db.Column(db.String(100), nullable=False)
    is_demo_model = db.Column(db.Boolean, default=True, nullable=False)
    human_verified = db.Column(db.Boolean, default=False, nullable=False)
    limitations_disclaimer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "original_filename": self.original_filename,
            "file_size_kb": self.file_size_kb,
            "predicted_category": self.predicted_category,
            "confidence_score": self.confidence_score,
            "model_version": self.model_version,
            "is_demo_model": self.is_demo_model,
            "human_verified": self.human_verified,
            "limitations_disclaimer": self.limitations_disclaimer,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "image_url": f"/uploads/{self.filename}"
        }


class AuditEvent(db.Model):
    """
    System audit trail for administrative actions, incident report submissions,
    and external data fetch events.
    """
    __tablename__ = "audit_events"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False, index=True)
    details = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, default=utc_now, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "action": self.action,
            "details": self.details,
            "ip_address": self.ip_address,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
