using System;
using System.Collections.Generic;
using System.Text;
using DDD.CarRental.Core.DomainModelLayer.Models;
using DDD.SharedKernel.DomainModelLayer;

namespace DDD.CarRental.Core.DomainModelLayer.Factories
{

    public class RentalFactory
    {
        private IDomainEventPublisher _domainEventPublisher;

        public RentalFactory(IDomainEventPublisher domainEventPublisher)
        {
            this._domainEventPublisher = domainEventPublisher;
        }

        public Rental Create(long rentalId, DateTime started, Car car, Driver driver)
        {

            CheckIfCarIsFree(car);

            return new Rental(rentalId, car.Id, driver.Id, started);
        }



        private void CheckIfCarIsFree(Car car)
        {
            if (car.Status != CarStatus.Free) 
                throw new Exception($"Car '{car.Id}' is not free");
        }
    }
}
