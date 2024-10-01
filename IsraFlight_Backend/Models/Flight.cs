namespace IsraelFlight_Backend.Models
{
    public class Flight
    {
        public int FlightID { get; set; }
        public int PlaneID { get; set; }
        public string DepartureLocation { get; set; }
        public string LandingLocation { get; set; }
        public DateTime DepartureDateTime { get; set; }
        public DateTime EstimatedLandingDateTime { get; set; }
        public decimal FlightPrice { get; set; }
      
    }
}
