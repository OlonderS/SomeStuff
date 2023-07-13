using DDD.CarRental.Core.DomainModelLayer.Models;

using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;

namespace DDD.CarRental.Core.DomainModelLayer.Events
{
    public class RentalFishedDomainEvent : DomainEvent
    {
        public Rental Rental { get; private set; }


        public RentalFishedDomainEvent(Rental rental)
        {
            Rental = rental;
        }
    }
}
