
using System.Linq.Expressions;
using Microsoft.EntityFrameworkCore;

namespace server.Repositories;

public class PostgreRepository<T>(AppDbContext dbContext) : IRepository<T> where T : class, IEntityPostgre
{
  public readonly AppDbContext _context = dbContext;
  public readonly DbSet<T> _dbSet = dbContext.Set<T>();

  public async Task CreateAsync(ICollection<T> entities)
  {
    await _dbSet.AddRangeAsync(entities);
    await _context.SaveChangesAsync();
  }

  public async Task DeleteAsync(ICollection<T> entities)
  {
    _dbSet.RemoveRange(entities);
    await _context.SaveChangesAsync();
  }

  public async Task<ICollection<T>> FindAsync(Expression<Func<T, bool>> predicate) =>
    await _dbSet.Where(predicate).ToListAsync();

  public async Task<ICollection<T>> GetAllAsync() =>
    await _dbSet.ToListAsync();

  public async Task UpdateAsync(ICollection<T> entities)
  {
    await Task.WhenAll(entities.Select(async entity =>
    {
      T? item = await _dbSet.FirstOrDefaultAsync(i => i.Id == entity.Id);
      if (item is null) return;

      _context.Entry(item).State = EntityState.Detached;
      _context.Attach(entity);
      _context.Entry(entity).State = EntityState.Modified;
    }));

    await _context.SaveChangesAsync();
  }

}