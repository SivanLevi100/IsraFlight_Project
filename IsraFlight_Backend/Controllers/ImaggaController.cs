using IsraelFlight_Backend.Services;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;

namespace IsraelFlight_Backend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ImaggaController : ControllerBase
    {
        private readonly ImaggaService _imaggaService;

        public ImaggaController(ImaggaService imaggaService)
        {
            _imaggaService = imaggaService;
        }

        [HttpPost("recognize-image")]
        public async Task<IActionResult> RecognizeImage([FromBody] string imageUrl)
        {
            if (string.IsNullOrEmpty(imageUrl))
            {
                return BadRequest("Image URL cannot be null or empty.");
            }

            var result = await _imaggaService.RecognizeImageAsync(imageUrl);
            return Ok(result);
        }
    }
}
