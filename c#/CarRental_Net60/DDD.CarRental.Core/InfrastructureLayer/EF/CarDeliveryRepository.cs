using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.CarRental.Core.DomainModelLayer.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.InfrastructureLayer.EF
{
    public class CarDeliveryRepository : Repository<CarDelivery>, ICarDeliveryRepository
    {
        public CarDeliveryRepository(CarRentalDbContext context)
            : base(context)
        { }
    }
}
