using System;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace IsraelFlight_Backend.Services
{
    public class ImaggaService
    {
        private readonly HttpClient _httpClient;
        private readonly string _apiKey = "acc_2e345ed4bd83ebb"; 
        private readonly string _apiSecret = "4c5091df2b47a29df5e6791f26564e1b";

   

        public ImaggaService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<bool> RecognizeImageAsync(string imageUrl)
        {
            try
            {
                var credentials = $"{_apiKey}:{_apiSecret}";
                var base64Credentials = Convert.ToBase64String(System.Text.Encoding.ASCII.GetBytes(credentials));

                _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Basic", base64Credentials);

                var url = $"https://api.imagga.com/v2/tags?image_url={Uri.EscapeDataString(imageUrl)}";
                var response = await _httpClient.GetAsync(url);

                if (!response.IsSuccessStatusCode)
                {
                    var errorMessage = await response.Content.ReadAsStringAsync();
                    throw new Exception($"Error from Imagga API: {response.StatusCode} - {errorMessage}");
                }

                var jsonResponse = await response.Content.ReadAsStringAsync();
                var parsedResponse = JObject.Parse(jsonResponse);

                // בדיקת תוויות המוחזרות
                var tags = parsedResponse["result"]["tags"]?.ToObject<List<JObject>>();
                if (tags != null)
                {
                    foreach (var tag in tags)
                    {
                        var tagName = tag["tag"]["en"]?.ToString();
                        if (string.Equals(tagName, "airplane", StringComparison.OrdinalIgnoreCase))    
                        {
                            return true; // התמונה מכילה מטוס
                        }
                    }
                }

                return false; // התמונה אינה מכילה מטוס
            }
            catch (Exception ex)
            {
                // לוג או טיפול בשגיאות
                throw new Exception("An error occurred while recognizing the image.", ex);
            }
        }

    }
}
