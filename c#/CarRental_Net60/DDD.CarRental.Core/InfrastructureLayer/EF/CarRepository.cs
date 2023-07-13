using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.CarRental.Core.DomainModelLayer.Models;
using DDD.CarRental.Core.InfrastructureLayer.EF;
using Microsoft.EntityFrameworkCore;
using System.Linq;

namespace DDD.CarRental.Core.InfrastructureLayer.EF
{
    public class CarRepository : Repository<Car>, ICarRepository
    { 
        public CarRepository(CarRentalDbContext context)
            :base(context)
        { }
    }
}
