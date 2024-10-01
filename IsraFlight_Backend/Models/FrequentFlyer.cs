namespace IsraelFlight_Backend.Models
{
    public class FrequentFlyer
    {
        public int FrequentFlyerID { get; set; }
        public string Username { get; set; }
        public string PasswordHash { get; set; }
        public string Email { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string PassportNumber { get; set; }
        public DateTime DateOfBirth { get; set; }
    }
}
