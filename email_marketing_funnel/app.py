from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from models import db, Subscriber, Campaign, CampaignSend, EmailTemplate, Workflow, PerformanceLog
from config import Config
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# ─────────────────────────────────────────────
# Helper: seed sample data
# ─────────────────────────────────────────────
def seed_data():
    if Subscriber.query.first():
        return  # already seeded

    # Sample subscribers
    names = ["Aarav Sharma", "Priya Patel", "Rohan Gupta", "Ananya Singh", "Vikram Mehta",
             "Sneha Reddy", "Karan Malhotra", "Neha Joshi", "Aditya Verma", "Isha Kapoor"]
    for i, name in enumerate(names):
        sub = Subscriber(
            email=f"user{i+1}@example.com",
            name=name,
            status="active" if i < 9 else "unsubscribed",
            source="website" if i % 2 == 0 else "referral"
        )
        db.session.add(sub)

    # Extra subscribers for chart growth
    for i in range(11, 45):
        sub = Subscriber(
            email=f"subscriber{i}@mail.com",
            name=f"User {i}",
            status="active",
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 60))
        )
        db.session.add(sub)

    # Email Templates
    templates = [
        EmailTemplate(
            name="Welcome",
            category="welcome",
            subject="Welcome to Uncodemy Digital Marketing!",
            body_html="""
            <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
                <h2 style="color:#2563eb;">Welcome aboard! 🎉</h2>
                <p>Thank you for joining our community. Start your digital marketing journey today.</p>
                <p><a href="https://uncodemy.com/course/digital-marketing-training-course-in-noida" 
                      style="background:#2563eb;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;">
                      Explore Noida Course</a></p>
            </div>
            """
        ),
        EmailTemplate(
            name="Newsletter",
            category="newsletter",
            subject="Weekly Digital Marketing Insights",
            body_html="""
            <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;">
                <h2>This Week in Digital Marketing</h2>
                <p>Latest trends, tips and course updates from Uncodemy.</p>
                <p><a href="https://uncodemy.com/course/digital-marketing-training-course-in-delhi">Delhi Batch Open</a></p>
            </div>
            """
        ),
        EmailTemplate(
            name="Special Offer",
            category="offer",
            subject="🔥 Limited Time: 30% Off Digital Marketing Course",
            body_html="""
            <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;text-align:center;">
                <h1 style="color:#1e40af;">Special Offer</h1>
                <p style="font-size:18px;">Don't miss this opportunity!</p>
                <p>Enroll in Uncodemy's Digital Marketing Training and transform your career.</p>
                <div style="margin:24px 0;">
                    <a href="https://uncodemy.com/course/digital-marketing-training-course-in-noida"
                       style="background:#2563eb;color:white;padding:14px 28px;text-decoration:none;border-radius:8px;margin:8px;display:inline-block;">
                       Noida Batch – Enroll Now</a>
                    <a href="https://uncodemy.com/course/digital-marketing-training-course-in-delhi"
                       style="background:#059669;color:white;padding:14px 28px;text-decoration:none;border-radius:8px;margin:8px;display:inline-block;">
                       Delhi Batch – Enroll Now</a>
                </div>
            </div>
            """
        ),
    ]
    for t in templates:
        db.session.add(t)

    # Sample Campaign (Special Offer)
    campaign = Campaign(
        title="Special Offer – Digital Marketing Course",
        subject="🔥 Don't Miss This Opportunity – 30% Off!",
        body_html=templates[2].body_html,
        cta_text="Shop Now",
        cta_url="https://uncodemy.com/course/digital-marketing-training-course-in-noida",
        status="active",
        opens=18,
        clicks=8,
        unsubscribes=1,
        sent_at=datetime.utcnow() - timedelta(days=2)
    )
    db.session.add(campaign)
    db.session.flush()

    # Create some sends for the campaign
    subs = Subscriber.query.limit(40).all()
    for sub in subs:
        send = CampaignSend(
            campaign_id=campaign.id,
            subscriber_id=sub.id,
            opened=random.choice([True, False, False]),
            clicked=random.choice([True, False, False, False]),
            unsubscribed=(sub.status == "unsubscribed")
        )
        db.session.add(send)

    # Workflow
    workflow = Workflow(
        name="Welcome → Wait → Offer",
        description="New subscriber gets Welcome email, waits 2 days, then Special Offer if engaged.",
        trigger="new_subscriber",
        is_active=True,
        steps=[
            {"type": "send_template", "template": "Welcome", "delay_days": 0},
            {"type": "wait", "days": 2},
            {"type": "condition", "if": "opened", "yes": "Special Offer", "no": "Newsletter"},
            {"type": "send_template", "template": "Special Offer"}
        ]
    )
    db.session.add(workflow)

    # Performance logs (last 7 days for chart)
    for i in range(7):
        log = PerformanceLog(
            date=(datetime.utcnow() - timedelta(days=6-i)).date(),
            opens=random.randint(8, 25),
            clicks=random.randint(3, 12),
            unsubscribes=random.randint(0, 2),
            new_subscribers=random.randint(2, 8)
        )
        db.session.add(log)

    db.session.commit()
    print("✅ Sample data seeded successfully!")


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────
@app.route('/')
def dashboard():
    # Stats
    total_subs = Subscriber.query.filter_by(status='active').count()
    total_campaigns = Campaign.query.count()
    active_workflows = Workflow.query.filter_by(is_active=True).count()

    # Latest campaign for the left card
    campaign = Campaign.query.filter_by(status='active').first()
    if not campaign:
        campaign = Campaign.query.first()

    # Templates for middle card
    templates = EmailTemplate.query.all()

    # Workflow
    workflow = Workflow.query.filter_by(is_active=True).first()

    # Performance metrics
    if campaign:
        open_rate = campaign.open_rate()
        click_rate = campaign.click_rate()
        unsub_rate = round((campaign.unsubscribes / max(len(campaign.sends), 1)) * 100, 1)
    else:
        open_rate, click_rate, unsub_rate = 45.0, 20.0, 1.0

    # Subscriber growth for bar chart (last 7 days)
    logs = PerformanceLog.query.order_by(PerformanceLog.date).limit(7).all()
    chart_data = [log.new_subscribers for log in logs] if logs else [2, 4, 6, 5, 8, 9, 12]

    return render_template(
        'dashboard.html',
        campaign=campaign,
        templates=templates,
        workflow=workflow,
        open_rate=open_rate,
        click_rate=click_rate,
        unsub_rate=unsub_rate,
        total_subs=total_subs,
        chart_data=chart_data,
        total_campaigns=total_campaigns,
        active_workflows=active_workflows
    )


@app.route('/campaign/<int:id>')
def view_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    return render_template('campaign_detail.html', campaign=campaign)


@app.route('/campaign/create', methods=['GET', 'POST'])
def create_campaign():
    if request.method == 'POST':
        title = request.form.get('title')
        subject = request.form.get('subject')
        body = request.form.get('body_html')
        cta_text = request.form.get('cta_text', 'Shop Now')
        cta_url = request.form.get('cta_url')
        status = request.form.get('status', 'draft')

        campaign = Campaign(
            title=title,
            subject=subject,
            body_html=body,
            cta_text=cta_text,
            cta_url=cta_url,
            status=status
        )
        db.session.add(campaign)
        db.session.commit()
        flash('Campaign created successfully!', 'success')
        return redirect(url_for('dashboard'))

    templates = EmailTemplate.query.all()
    return render_template('create_campaign.html', templates=templates)


@app.route('/campaign/<int:id>/send', methods=['POST'])
def send_campaign(id):
    campaign = Campaign.query.get_or_404(id)
    active_subs = Subscriber.query.filter_by(status='active').all()

    for sub in active_subs:
        # avoid duplicate sends
        existing = CampaignSend.query.filter_by(campaign_id=campaign.id, subscriber_id=sub.id).first()
        if not existing:
            send = CampaignSend(campaign_id=campaign.id, subscriber_id=sub.id)
            db.session.add(send)

    campaign.status = 'sent'
    campaign.sent_at = datetime.utcnow()
    db.session.commit()
    flash(f'Campaign sent to {len(active_subs)} subscribers!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/campaign/<int:id>/track_open')
def track_open(id):
    campaign = Campaign.query.get_or_404(id)
    campaign.opens += 1
    db.session.commit()
    return '', 204


@app.route('/campaign/<int:id>/track_click')
def track_click(id):
    campaign = Campaign.query.get_or_404(id)
    campaign.clicks += 1
    db.session.commit()
    # Redirect to the actual CTA
    return redirect(campaign.cta_url or 'https://uncodemy.com/course/digital-marketing-training-course-in-noida')


@app.route('/templates')
def list_templates():
    templates = EmailTemplate.query.all()
    return render_template('templates.html', templates=templates)


@app.route('/templates/<int:id>')
def view_template(id):
    template = EmailTemplate.query.get_or_404(id)
    return render_template('template_detail.html', template=template)


@app.route('/templates/create', methods=['GET', 'POST'])
def create_template():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        subject = request.form.get('subject')
        body = request.form.get('body_html')

        t = EmailTemplate(name=name, category=category, subject=subject, body_html=body)
        db.session.add(t)
        db.session.commit()
        flash('Template created!', 'success')
        return redirect(url_for('list_templates'))

    return render_template('create_template.html')


@app.route('/workflows')
def list_workflows():
    workflows = Workflow.query.all()
    return render_template('workflows.html', workflows=workflows)


@app.route('/workflows/<int:id>/toggle', methods=['POST'])
def toggle_workflow(id):
    wf = Workflow.query.get_or_404(id)
    wf.is_active = not wf.is_active
    db.session.commit()
    flash(f'Workflow {"activated" if wf.is_active else "deactivated"}!', 'success')
    return redirect(url_for('list_workflows'))


@app.route('/subscribers')
def list_subscribers():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    query = Subscriber.query
    if status != 'all':
        query = query.filter_by(status=status)
    pagination = query.order_by(Subscriber.created_at.desc()).paginate(page=page, per_page=15)
    return render_template('subscribers.html', pagination=pagination, current_status=status)


@app.route('/subscribers/add', methods=['GET', 'POST'])
def add_subscriber():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        if Subscriber.query.filter_by(email=email).first():
            flash('Email already exists!', 'error')
            return redirect(url_for('add_subscriber'))

        sub = Subscriber(email=email, name=name)
        db.session.add(sub)
        db.session.commit()
        flash('Subscriber added successfully!', 'success')
        return redirect(url_for('list_subscribers'))

    return render_template('add_subscriber.html')


@app.route('/subscribers/<int:id>/unsubscribe', methods=['POST'])
def unsubscribe(id):
    sub = Subscriber.query.get_or_404(id)
    sub.status = 'unsubscribed'
    db.session.commit()
    flash(f'{sub.email} unsubscribed.', 'success')
    return redirect(url_for('list_subscribers'))


@app.route('/api/stats')
def api_stats():
    """JSON endpoint for live dashboard refresh"""
    campaign = Campaign.query.filter_by(status='active').first()
    total_subs = Subscriber.query.filter_by(status='active').count()
    logs = PerformanceLog.query.order_by(PerformanceLog.date).limit(7).all()
    return jsonify({
        'open_rate': campaign.open_rate() if campaign else 45,
        'click_rate': campaign.click_rate() if campaign else 20,
        'unsub_rate': 1.0,
        'total_subs': total_subs,
        'chart_data': [l.new_subscribers for l in logs]
    })


@app.route('/shop-now')
def shop_now():
    """CTA landing – shows both Uncodemy course options"""
    return render_template('shop_now.html')


# ─────────────────────────────────────────────
# CLI / Init
# ─────────────────────────────────────────────
@app.cli.command('init-db')
def init_db():
    """Initialize the database and seed sample data."""
    db.create_all()
    seed_data()
    print("Database initialized.")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, host='0.0.0.0', port=5000)
