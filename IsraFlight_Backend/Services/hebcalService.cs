using System;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

public class HebcalService
{
    private readonly HttpClient _httpClient;
    private const string BaseUrl = "https://www.hebcal.com/hebcal";

    public HebcalService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    
    public async Task<bool> IsDateBetweenCandleLightingAndHavdalah(DateTime date)
    {
        Console.WriteLine($"Landing Time: {date}");
        var items = await GetShabbatItems(date);
        foreach (var item in items)
        {
            Console.WriteLine(item.ToString());
        }

        for (int i = 0; i < items.Count - 1; i++)
        {
            var currentItem = items[i];
            var nextItem = items[i + 1];

            if (currentItem["category"].ToString() == "candles" && nextItem["category"].ToString() == "havdalah")
            {
                DateTime candleLightingTime = DateTime.Parse(currentItem["date"].ToString());
                DateTime havdalahTime = DateTime.Parse(nextItem["date"].ToString());
                Console.WriteLine($"Shabbat starts at: {candleLightingTime}");
                Console.WriteLine($"Shabbat ends at: {havdalahTime}");

                if (date >= candleLightingTime && date <= havdalahTime)
                {
                    return true;
                }
            }
        }

        return false;
    }
    private async Task<JArray> GetShabbatItems(DateTime date)
    {
        var response = await _httpClient.GetStringAsync($"{BaseUrl}?v=1&cfg=json&year={date.Year}&month={date.Month}&day={date.Day}&c=on&geo=geoname&geonameid=293397");
        //var response = await _httpClient.GetStringAsync($"{BaseUrl}?v=1&cfg=json&year={date.Year}&month={date.Month}&day={date.Day}&c=on&geo=geoname&geonameid=3448439"");
        Console.WriteLine($"API Response: {response}");
        //var response = await _httpClient.GetStringAsync($"{BaseUrl}?v=1&cfg=json&year={date.Year}&month={date.Month}&day={date.Day}&c=on&geo=geoname&geonameid=3448439");
        var jsonResponse = JObject.Parse(response);
        return jsonResponse["items"].ToObject<JArray>();
    }


    
    public async Task<string> GetParashaForDate(DateTime date)
    {
        try
        {
            // חשב את התאריך של השבת הקרובה עבור התאריך שניתן
            var dayOfWeek = (int)date.DayOfWeek;
            var daysUntilSaturday = (6 - dayOfWeek + 7) % 7; // מסביר את המספר של הימים עד שבת
            var nextShabbatDate = date.AddDays(daysUntilSaturday);

            // בצע בקשה ל-API של Hebcal לקבלת פרשת השבוע עבור השבת הקרובה
            var response = await _httpClient.GetStringAsync(
                $"https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&M=on&gy={nextShabbatDate.Year}&gm={nextShabbatDate.Month}&gd={nextShabbatDate.Day}"
            );

            // פרס את המידע שהתקבל ל-JSON
            var jsonResponse = JObject.Parse(response);

            // מוציא את רשימת הפריטים מהתגובה
            var items = jsonResponse["items"].ToObject<JArray>();
            Console.WriteLine($"API Response: {items}");

            // מחפש את פרשת השבוע בתוך הקטגוריות
            var parasha = items
                .Where(i => i["category"].ToString() == "parashat")
                .Select(i => i["title"].ToString())
                .FirstOrDefault();

            // אם לא נמצאה פרשה, נשלח הודעת שגיאה
            if (string.IsNullOrEmpty(parasha))
            {
                throw new Exception("No Parasha found for this date.");
            }

            return parasha;
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error retrieving Parasha: {ex.Message}");
            throw;
        }
    }

    public class ShabbatTimes
    {
        public DateTime CandleLighting { get; set; }
        public DateTime Havdalah { get; set; }
    }

    public async Task<ShabbatTimes> GetCandleLightingAndHavdalahTimes(DateTime date)
    {
        try
        {
            // Calculate the date of the upcoming Saturday for the given date
            var dayOfWeek = (int)date.DayOfWeek;
            var daysUntilSaturday = (6 - dayOfWeek + 7) % 7;
            var nextShabbatDate = date.AddDays(daysUntilSaturday);

            // Make a request to the Hebcal API to get the Shabbat times for the upcoming Saturday
            var response = await _httpClient.GetStringAsync(
                $"https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&M=on&gy={nextShabbatDate.Year}&gm={nextShabbatDate.Month}&gd={nextShabbatDate.Day}"
            );

            // Parse the received information to JSON
            var jsonResponse = JObject.Parse(response);

            // Extract the list of items from the response
            var items = jsonResponse["items"].ToObject<JArray>();
            Console.WriteLine($"API Response: {items}");

            // Search for candle lighting and havdalah times within the categories
            DateTime? candleLightingTime = null;
            DateTime? havdalahTime = null;

            foreach (var item in items)
            {
                if (item["category"].ToString() == "candles")
                {
                    candleLightingTime = DateTime.Parse(item["date"].ToString());
                }
                else if (item["category"].ToString() == "havdalah")
                {
                    havdalahTime = DateTime.Parse(item["date"].ToString());
                }

                if (candleLightingTime.HasValue && havdalahTime.HasValue)
                {
                    break;
                }
            }

            // If either time is not found, throw an exception
            if (!candleLightingTime.HasValue || !havdalahTime.HasValue)
            {
                throw new Exception("Candle lighting or Havdalah time not found for this date.");
            }

            return new ShabbatTimes
            {
                CandleLighting = candleLightingTime.Value,
                Havdalah = havdalahTime.Value
            };
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error retrieving Shabbat times: {ex.Message}");
            throw;
        }
    }

}
//2024-01-20T17:40:00
