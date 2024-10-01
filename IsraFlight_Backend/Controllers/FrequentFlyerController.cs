using IsraelFlight_Backend.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace IsraelFlight_Backend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class FrequentFlyerController : ControllerBase
    {
        private readonly AirlineDbContext _context;

        public FrequentFlyerController(AirlineDbContext context)
        {
            _context = context;
        }

        // GET: api/FrequentFlyer
        [HttpGet]
        public async Task<ActionResult<IEnumerable<FrequentFlyer>>> GetFrequentFlyers()
        {
            return await _context.FrequentFlyer.ToListAsync();
        }

        // GET: api/FrequentFlyer/5
        [HttpGet("{id}")]
        public async Task<ActionResult<FrequentFlyer>> GetFrequentFlyer(int id)
        {
            var frequentFlyer = await _context.FrequentFlyer.FindAsync(id);

            if (frequentFlyer == null)
            {
                return NotFound();
            }

            return frequentFlyer;
        }

        // POST: api/FrequentFlyer
        [HttpPost]
        public async Task<ActionResult<FrequentFlyer>> PostFrequentFlyer(FrequentFlyer frequentFlyer)
        {
            _context.FrequentFlyer.Add(frequentFlyer);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetFrequentFlyer), new { id = frequentFlyer.FrequentFlyerID }, frequentFlyer);
        }

        // PUT: api/FrequentFlyer/5
        [HttpPut("{id}")]
        public async Task<IActionResult> PutFrequentFlyer(int id, FrequentFlyer frequentFlyer)
        {
            if (id != frequentFlyer.FrequentFlyerID)
            {
                return BadRequest();
            }

            _context.Entry(frequentFlyer).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!FrequentFlyerExists(id))
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

        // DELETE: api/FrequentFlyer/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteFrequentFlyer(int id)
        {
            var frequentFlyer = await _context.FrequentFlyer.FindAsync(id);

            if (frequentFlyer == null)
            {
                return NotFound();
            }

            _context.FrequentFlyer.Remove(frequentFlyer);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool FrequentFlyerExists(int id)
        {
            return _context.FrequentFlyer.Any(e => e.FrequentFlyerID == id);
        }
    }
}
