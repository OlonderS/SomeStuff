using DDD.SharedKernel.DomainModelLayer.Implementations;
using DDD.SharedKernel.DomainModelLayer;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.DomainModelLayer.Models
{
    public  class CarDelivery : Entity, IAggregateRoot
    {
        public long RentalId { get; set; }
        public Distance Distance { get; set; }

        public DateTime DateTime { get; set; }

        public CarDelivery()
        {
        }
        public CarDelivery(long rentalId, Distance distance, DateTime dateTime):base(rentalId)
        {
            
            Distance = distance;
            DateTime = dateTime;
        }

       
        

    }
}
