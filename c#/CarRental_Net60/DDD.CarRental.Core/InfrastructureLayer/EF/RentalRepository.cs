using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.CarRental.Core.DomainModelLayer.Models;

namespace DDD.CarRental.Core.InfrastructureLayer.EF
{
    public class RentalRepository : Repository<Rental>, IRentalRepository
    {
        public RentalRepository(CarRentalDbContext context)
            : base(context)
        { }
    }
}
