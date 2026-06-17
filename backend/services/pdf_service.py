import io
from typing import List
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors

from backend.models import ChatSession, ChatMessage


def generate_chat_export_pdf(session: ChatSession, messages: List[ChatMessage]) -> io.BytesIO:
    """
    Generates a PDF document from a chat session and its messages.
    Returns a BytesIO buffer containing the PDF data.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        rightMargin=72, 
        leftMargin=72,
        topMargin=72, 
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = styles['Title']
    
    user_label_style = ParagraphStyle(
        'UserLabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#2563eb"),  # Blue-600
        spaceAfter=4
    )
    
    ai_label_style = ParagraphStyle(
        'AILabelStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0f172a"),  # Slate-900
        spaceAfter=4
    )
    
    message_style = ParagraphStyle(
        'MessageStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        textColor=colors.HexColor("#334155"),  # Slate-700
        spaceAfter=16,
        leading=14
    )
    
    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Italic'],
        textColor=colors.HexColor("#64748b"),  # Slate-500
        spaceAfter=4
    )

    story = []
    
    # Title and Metadata
    story.append(Paragraph("LegalEase Consultation Report", title_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph(f"<b>Session Topic:</b> {session.title}", meta_style))
    created_str = session.created_at.strftime('%B %d, %Y at %I:%M %p') if session.created_at else "Unknown Date"
    story.append(Paragraph(f"<b>Date:</b> {created_str}", meta_style))
    
    story.append(Spacer(1, 24))
    
    # Messages
    for msg in messages:
        # Convert newlines to reportlab's <br/> tags
        safe_content = str(msg.content).replace("<", "&lt;").replace(">", "&gt;")
        formatted_content = safe_content.replace('\n', '<br />')
        
        if msg.role == 'user':
            story.append(Paragraph("Client Query", user_label_style))
            story.append(Paragraph(formatted_content, message_style))
        elif msg.role == 'assistant':
            story.append(Paragraph("LegalEase AI", ai_label_style))
            story.append(Paragraph(formatted_content, message_style))
            
    doc.build(story)
    
    # Reset buffer position to beginning
    buffer.seek(0)
    return buffer
