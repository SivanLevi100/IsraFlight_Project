namespace IsraelFlight_Backend.Models
{
    public class Ticket
    {
        public string TicketID { get; set; }
        public int BookingID { get; set; }
        public string FlightID { get; set; }
        public string DepartureLocation { get; set; }
        public string LandingLocation { get; set; }
        public DateTime DepartureDateTime { get; set; }
        public DateTime EstimatedLandingDateTime { get; set; }
        public string TicketURL { get; set; }

        public Booking Booking { get; set; }
    }
}
