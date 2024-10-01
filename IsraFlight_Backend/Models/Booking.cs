namespace IsraelFlight_Backend.Models
{
    public class Booking
    {
        public int BookingID { get; set; }
        public int FlightID { get; set; }
        public int FrequentFlyerID { get; set; }
        public DateTime BookingDate { get; set; }
        public string TicketID { get; set; }
        public decimal FlightPrice { get; set; }

       
    }
}
