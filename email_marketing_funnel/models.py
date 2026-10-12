from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, unsubscribed
    source = db.Column(db.String(50), default='website')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    campaigns = db.relationship('CampaignSend', backref='subscriber', lazy=True)

    def __repr__(self):
        return f'<Subscriber {self.email}>'

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body_html = db.Column(db.Text, nullable=False)
    cta_text = db.Column(db.String(100), default='Shop Now')
    cta_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='draft')  # draft, scheduled, sent, active
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    opens = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    unsubscribes = db.Column(db.Integer, default=0)
    sends = db.relationship('CampaignSend', backref='campaign', lazy=True)

    def open_rate(self):
        total = len(self.sends) or 1
        return round((self.opens / total) * 100, 1)

    def click_rate(self):
        total = len(self.sends) or 1
        return round((self.clicks / total) * 100, 1)

    def __repr__(self):
        return f'<Campaign {self.title}>'

class CampaignSend(db.Model):
    __tablename__ = 'campaign_sends'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscribers.id'), nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    opened = db.Column(db.Boolean, default=False)
    clicked = db.Column(db.Boolean, default=False)
    unsubscribed = db.Column(db.Boolean, default=False)

class EmailTemplate(db.Model):
    __tablename__ = 'email_templates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # welcome, newsletter, offer, etc.
    subject = db.Column(db.String(200))
    body_html = db.Column(db.Text)
    thumbnail = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Template {self.name}>'

class Workflow(db.Model):
    __tablename__ = 'workflows'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    trigger = db.Column(db.String(50), default='new_subscriber')  # new_subscriber, tag, etc.
    is_active = db.Column(db.Boolean, default=True)
    steps = db.Column(db.JSON)  # list of steps: template_id, wait_days, condition, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Workflow {self.name}>'

class PerformanceLog(db.Model):
    __tablename__ = 'performance_logs'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    opens = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    unsubscribes = db.Column(db.Integer, default=0)
    new_subscribers = db.Column(db.Integer, default=0)
