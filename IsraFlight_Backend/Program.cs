using IsraelFlight_Backend.Models;
using IsraelFlight_Backend.Services;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// הוספת ה-DbContext עם מחרוזת החיבור ממערך ההגדרות
builder.Services.AddDbContext<AirlineDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// הוספת השירותים החדשים (HebcalService ו-ImaggaService)
builder.Services.AddHttpClient<HebcalService>();
builder.Services.AddHttpClient<ImaggaService>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
