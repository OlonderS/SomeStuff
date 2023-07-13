using DDD.SharedKernel.InfrastructureLayer;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;

namespace DDD.CarRental.Core.InfrastructureLayer.EF
{
    public class Repository<TEntity> : IRepository<TEntity> where TEntity : class
    {
        protected readonly CarRentalDbContext _context;
        public Repository(CarRentalDbContext context)
        {
            _context = context;
        }
        public TEntity Get(long id)
        {
            return _context.Set<TEntity>().Find(id);
        }
        public IList<TEntity> GetAll()
        {
            return _context.Set<TEntity>().ToList();
        }
        public IList<TEntity> Find(Expression<Func<TEntity, bool>> expression)
        {
            return _context.Set<TEntity>().Where(expression).ToList();
        }
        public void Insert(TEntity entity)
        {
            _context.Set<TEntity>().Add(entity);
        }
        public void Delete(TEntity entity)
        {
            _context.Set<TEntity>().Remove(entity);
        }
    }
}
