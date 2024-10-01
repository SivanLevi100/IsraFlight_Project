namespace IsraelFlight_Backend.Models
{
    public class Plane
    {
        public int PlaneID { get; set; }
        public string Manufacturer { get; set; }
        public string Model { get; set; }
        public int YearOfManufacture { get; set; }
        public string Nickname { get; set; }
        public string ImageURL { get; set; }
    }
}
