using IsraelFlight_Backend.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;

namespace IsraelFlight_Backend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class FlightController : ControllerBase
    {
        private readonly AirlineDbContext _context;

        public FlightController(AirlineDbContext context)
        {
            _context = context;
        }

        // GET: api/Flight
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Flight>>> GetFlights()
        {
            return await _context.Flight.ToListAsync();
        }

        // GET: api/Flight/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Flight>> GetFlight(int id)
        {
            var flight = await _context.Flight.FindAsync(id);

            if (flight == null)
            {
                return NotFound();
            }

            return flight;
        }

        // POST: api/Flight
        [HttpPost]
        public async Task<ActionResult<Flight>> PostFlight(Flight flight)
        {
            // בדיקה אם FlightID כבר קיים
            var existingFlight = await _context.Flight.FindAsync(flight.FlightID);
            if (existingFlight != null)
            {
                return Conflict($"Flight with ID {flight.FlightID} already exists.");
            }

            // בדיקה אם PlaneID קיים בטבלת Plane
            var plane = await _context.Plane.FindAsync(flight.PlaneID);
            if (plane == null)
            {
                return BadRequest($"Plane with ID {flight.PlaneID} does not exist.");
            }

            // הוספת הטיסה אם PlaneID קיים ו-FlightID לא קיים
            _context.Flight.Add(flight);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetFlight), new { id = flight.FlightID }, flight);
        }


        // PUT: api/Flight/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutFlight(int id, Flight flight)
        {
            if (id != flight.FlightID)
            {
                return BadRequest();
            }

            _context.Entry(flight).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!FlightExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // DELETE: api/Flight/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFlight(int id)
        {
            var flight = await _context.Flight.FindAsync(id);

            if (flight == null)
            {
                return NotFound();
            }

            _context.Flight.Remove(flight);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool FlightExists(int id)
        {
            return _context.Flight.Any(e => e.FlightID == id);
        }
    }
}
    
