using Microsoft.EntityFrameworkCore;

namespace IsraelFlight_Backend.Models

{
    public class AirlineDbContext : DbContext
    {
        public AirlineDbContext(DbContextOptions<AirlineDbContext> options) : base(options)
        {
        }

        public DbSet<Admin> Admin { get; set; }
        public DbSet<FrequentFlyer> FrequentFlyer { get; set; }
        public DbSet<Plane> Plane { get; set; }
        public DbSet<Flight> Flight { get; set; }
        public DbSet<Booking> Booking { get; set; }
        public DbSet<Airport> Airport { get; set; }
        public DbSet<Ticket> Ticket { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Add additional configurations here if needed

            base.OnModelCreating(modelBuilder);
        }
    }

}