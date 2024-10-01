using IsraelFlight_Backend.Services;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Threading.Tasks;

namespace IsraelFlight_Backend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class HebcalController : ControllerBase
    {
        private readonly HebcalService _hebcalService;

        public HebcalController(HebcalService hebcalService)
        {
            _hebcalService = hebcalService;
        }

        [HttpGet("parasha")]
        public async Task<IActionResult> GetParasha([FromQuery] DateTime date)
        {
            try
            {
                var parasha = await _hebcalService.GetParashaForDate(date);
                return Ok(parasha);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

        [HttpGet("is-flight-during-shabbat")]
        public async Task<IActionResult> IsFlightDuringShabbat([FromBody] DateTime landingTime)
        {
            try
            {
                var isDuringShabbat = await _hebcalService.IsDateBetweenCandleLightingAndHavdalah(landingTime);
                return Ok(isDuringShabbat);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

        [HttpGet("shabbat-times")]
        public async Task<IActionResult> GetShabbatTimes([FromQuery] DateTime date)
        {
            try
            {
                var shabbatTimes = await _hebcalService.GetCandleLightingAndHavdalahTimes(date);
                return Ok(shabbatTimes);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }
    }
}
