from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.graphics.barcode import code128
from controllers.services_controller import HebcalController
from datetime import datetime

def create_ticket_pdf(ticket, file_path, frequentFlyer):
    """
    Create a PDF ticket for a flight.

    Args:
        ticket: The ticket object containing flight details.
        file_path (str): The path where the PDF file will be saved.
        frequentFlyer: The frequent flyer object containing passenger details.

    Returns:
        str: The file path of the created PDF.

    Raises:
        Exception: If there's an error during PDF creation.
    """
    try:
        # Initialize the canvas
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Define colors
        main_color = colors.Color(0.2, 0.4, 0.6)  # Dark blue
        accent_color = "#C8E9FF"  # Light grey

        # Create background
        c.setFillColor(colors.white)
        c.rect(0, 0, width, height, fill=1)

        # Create top header
        c.setFillColor(accent_color)
        c.rect(0, height - 2*inch, width, 2*inch, fill=1)

        # Add company logo
        logo_path = 'IsraelFlight_Fronted_6419_6037\Images\IsraelFlight_logo_without.png'
        try:
            c.drawImage(logo_path, 0.5*inch, height - 1.75*inch, width=1.5*inch, height=1.5*inch, mask='auto', preserveAspectRatio=True, anchor='c')
        except Exception as e:
            print(f"Error loading logo: {e}")
            c.setFont("Helvetica-Bold", 24)
            c.setFillColor(colors.white)
            c.drawString(0.5*inch, height - 1.25*inch, "IsraFlight")

        # Add airline name and ticket type
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor("#004aad")
        c.drawString(3*inch, height - 1*inch, "ISRAFLIGHT")
        c.setFont("Helvetica", 14)
        c.drawString(3*inch, height - 1.3*inch, "BOARDING PASS")

        # Create main content area
        c.setFillColor(colors.white)
        c.rect(0.5*inch, 1*inch, width - 1*inch, height - 3*inch, fill=1)

        # Draw white border around the content area
        c.setStrokeColor(colors.white)
        c.setLineWidth(2)
        c.rect(0.5*inch, 1*inch, width - 1*inch, height - 3*inch, fill=0)

        # Add flight information
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(main_color)
        c.drawString(1*inch, height - 3*inch, "FLIGHT")
        c.drawString(3*inch, height - 3*inch, "FROM")
        c.drawString(5*inch, height - 3*inch, "TO")
        
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 3.3*inch, str(ticket.flightId))
        c.drawString(3*inch, height - 3.3*inch, str(ticket.departureLocation))
        c.drawString(5*inch, height - 3.3*inch, str(ticket.landingLocation))

        # Add passenger information
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, height - 4*inch, "PASSENGER NAME")
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 4.3*inch, f"{frequentFlyer.firstName} {frequentFlyer.lastName}")

        # Add date and time information
        c.setFont("Helvetica-Bold", 14)
        c.drawString(1*inch, height - 5*inch, "DATE")
        c.drawString(3*inch, height - 5*inch, "DEPARTURE")
        c.drawString(5*inch, height - 5*inch, "ARRIVAL")
        
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 5.3*inch, ticket.departureDatetime.strftime('%Y-%m-%d'))
        c.drawString(3*inch, height - 5.3*inch, ticket.departureDatetime.strftime('%H:%M'))
        c.drawString(5*inch, height - 5.3*inch, ticket.estimatedLandingDatetime.strftime('%H:%M'))

        # Add booking and ticket ID
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1*inch, height - 6*inch, "BOOKING ID:")
        c.drawString(3*inch, height - 6*inch, "TICKET ID:")
        c.setFont("Helvetica", 10)
        c.drawString(1*inch, height - 6.2*inch, str(ticket.bookingId))
        c.drawString(3*inch, height - 6.2*inch, str(ticket.ticketId))

        # Add Parasha information
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(main_color)
        c.drawString(1*inch, height - 7*inch, "PARASHAT HASHAVUA:")
        c.setFont("Helvetica", 12)
        print(f"PARASHAT HASHAVUA:{str(HebcalController.get_parasha(ticket.estimatedLandingDatetime))}")
        c.drawString(3*inch, height - 7*inch, str(HebcalController.get_parasha(ticket.estimatedLandingDatetime)))

        # Add Shabbat times
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, height - 7.5*inch, "SHABBAT TIMES:")
        c.setFont("Helvetica", 10)
        shabbat_times = HebcalController.get_shabbat_times(ticket.estimatedLandingDatetime)   
        if shabbat_times:
           c.drawString(1*inch, height - 7.8*inch, f"Candle Lighting: {format_date(shabbat_times['candleLighting'])}")
           c.drawString(1*inch, height - 8.1*inch, f"Havdalah: {format_date(shabbat_times['havdalah'])}")
        else:
            c.drawString(1*inch, height - 7.8*inch, "Unable to retrieve Shabbat times")

        # Add barcode
        barcode_value = f"{ticket.ticketId}-{ticket.flightId}"
        barcode = code128.Code128(barcode_value, barHeight=0.5*inch, barWidth=1.1)
        barcode.drawOn(c, 1*inch, 1.5*inch)
        c.setFont("Helvetica", 8)
        c.drawString(1*inch, 1.3*inch, barcode_value)

        # Add tear-off line
        c.setDash(6, 3)
        c.setStrokeColor(accent_color)
        c.line(0.5*inch, 2.7*inch, width - 0.5*inch, 2.7*inch)

        # Add footer
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColor(colors.gray)
        c.drawString(1*inch, 0.75*inch, "This is your boarding pass. Please present this document at the airport.")
        c.drawString(1*inch, 0.5*inch, "Thank you for choosing IsraelFlight. We wish you a pleasant journey!")

        # Save the PDF
        c.save()
        print(f"PDF created successfully at {file_path}")
        return file_path

    except Exception as e:
        print(f"Error in create_ticket_pdf: {e}")
        print(f"Ticket details: {vars(ticket)}")
        print(f"FrequentFlyer details: {vars(frequentFlyer)}")
        raise

def format_date(date_string):
    """
    Parse and format a date string.

    Args:
        date_string (str): The date string to format.

    Returns:
        str: The formatted date string.
    """
    dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    return dt.strftime("%d/%m/%Y %H:%M")