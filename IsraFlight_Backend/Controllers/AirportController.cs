using IsraelFlight_Backend.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace IsraelFlight_Backend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AirportController : ControllerBase
    {
        private readonly AirlineDbContext _context;

        public AirportController(AirlineDbContext context)
        {
            _context = context;
        }

        // GET: api/Airport
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Airport>>> GetAirports()
        {
            return await _context.Airport.ToListAsync();
        }

        // GET: api/Airport/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Airport>> GetAirport(int id)
        {
            var airport = await _context.Airport.FindAsync(id);

            if (airport == null)
            {
                return NotFound();
            }

            return airport;
        }

        // POST: api/Airport
        [HttpPost]
        public async Task<ActionResult<Airport>> PostAirport(Airport airport)
        {
            _context.Airport.Add(airport);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetAirport), new { id = airport.AirportID }, airport);
        }

        // PUT: api/Airport/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutAirport(int id, Airport airport)
        {
            if (id != airport.AirportID)
            {
                return BadRequest();
            }

            _context.Entry(airport).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!AirportExists(id))
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

        // DELETE: api/Airport/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteAirport(int id)
        {
            var airport = await _context.Airport.FindAsync(id);

            if (airport == null)
            {
                return NotFound();
            }

            _context.Airport.Remove(airport);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool AirportExists(int id)
        {
            return _context.Airport.Any(e => e.AirportID == id);
        }
    }
}
