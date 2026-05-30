using System.Linq.Expressions;
using MongoDB.Driver;

namespace server.Repositories;

public interface IRepository<T>
{
  Task<ICollection<T>> GetAllAsync();
  Task<ICollection<T>> FindAsync(Expression<Func<T, bool>> predicate);
  Task CreateAsync(ICollection<T> entities);
  Task UpdateAsync(ICollection<T> entities);
  Task DeleteAsync(ICollection<T> entities);
}