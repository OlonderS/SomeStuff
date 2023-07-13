using DDD.CarRental.Core.DomainModelLayer.Models;
using DDD.SharedKernel.InfrastructureLayer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.DomainModelLayer.Interfaces
{
    public interface ICarDeliveryRepository : IRepository<CarDelivery>
    {
    }
}
