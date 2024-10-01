using IsraelFlight_Backend.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace IsraelFlight_Backend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class PlaneController : ControllerBase
    {
        private readonly AirlineDbContext _context;

        public PlaneController(AirlineDbContext context)
        {
            _context = context;
        }

        // GET: api/Plane
        [HttpGet]
        public async Task<ActionResult<IEnumerable<Plane>>> GetPlanes()
        {
            return await _context.Plane.ToListAsync();
        }

        // GET: api/Plane/5
        [HttpGet("{id}")]
        public async Task<ActionResult<Plane>> GetPlane(int id)
        {
            var plane = await _context.Plane.FindAsync(id);

            if (plane == null)
            {
                return NotFound();
            }

            return plane;
        }

        // POST: api/Plane
        [HttpPost]
        public async Task<ActionResult<Plane>> PostPlane(Plane plane)
        {
            // בדיקה אם מטוס עם אותו ID כבר קיים
            var existingPlane = await _context.Plane.FindAsync(plane.PlaneID);
            if (existingPlane != null)
            {
                return Conflict($"Plane with ID {plane.PlaneID} already exists.");
            }

            // הוספת המטוס החדש אם ה-ID אינו קיים
            _context.Plane.Add(plane);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetPlane), new { id = plane.PlaneID }, plane);
        }

        // PUT: api/Plane/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutPlane(int id, Plane plane)
        {
            if (id != plane.PlaneID)
            {
                return BadRequest();
            }

            _context.Entry(plane).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!PlaneExists(id))
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

        // DELETE: api/Plane/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeletePlane(int id)
        {
            var plane = await _context.Plane.FindAsync(id);

            if (plane == null)
            {
                return NotFound();
            }

            _context.Plane.Remove(plane);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool PlaneExists(int id)
        {
            return _context.Plane.Any(e => e.PlaneID == id);
        }
    }
}
