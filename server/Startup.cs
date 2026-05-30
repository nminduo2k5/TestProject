using Microsoft.EntityFrameworkCore;
using server.Repositories;


namespace server;

public class Startup(IConfiguration configuration)
{
  public IConfiguration Configuration { get; } = configuration;

  void InitPostgre(IServiceCollection services)
  {

    services.AddDbContext<AppDbContext>(options =>
          options.UseNpgsql(Configuration.GetConnectionString("DefaultConnection")));
    services.AddScoped(typeof(IRepository<>), typeof(PostgreRepository<>));
  }

  public void ConfigureServices(IServiceCollection services)
  {
    services.AddCors(options =>
      options.AddDefaultPolicy(builder =>
        builder.AllowAnyHeader().AllowAnyMethod().AllowAnyOrigin()));
    services.AddControllers().AddNewtonsoftJson(options =>
        options.SerializerSettings.ReferenceLoopHandling = Newtonsoft.Json.ReferenceLoopHandling.Ignore);
    // services.AddControllers();
    services.AddEndpointsApiExplorer();
    services.AddSwaggerGen();

    InitPostgre(services);
    // InitMongoDb(services);
  }

  public void Configure(WebApplication app, IWebHostEnvironment env)
  {
    if (env.IsDevelopment()) app.UseSwagger().UseSwaggerUI();

    app.UseCors();
    // app.UseHttpsRedirection(); // Comment để tránh cảnh báo HTTPS redirection
    app.UseAuthorization();
    app.MapControllers();
  }
}