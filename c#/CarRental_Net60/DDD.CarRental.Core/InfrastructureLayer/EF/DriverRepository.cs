using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.CarRental.Core.DomainModelLayer.Models;
using System.Linq;

namespace DDD.CarRental.Core.InfrastructureLayer.EF
{
    public class DriverRepository : Repository<Driver>, IDriverRepository
    {
        public DriverRepository(CarRentalDbContext context)
            : base(context)
        { }

        public Driver GetDriverByLicenseNumber(string licenseNumber)
        {
            return _context.Drivers
                .Where(p => p.LicenseNumber == licenseNumber)
                .FirstOrDefault();
        }
    }
}
