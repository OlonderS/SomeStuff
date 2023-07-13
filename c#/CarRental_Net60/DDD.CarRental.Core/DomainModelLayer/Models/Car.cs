using DDD.SharedKernel.DomainModelLayer;
using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;

namespace DDD.CarRental.Core.DomainModelLayer.Models
{
    public enum CarStatus
    {
        Free = 0,
        Reserved = 1,
        Rented = 2
    }
    public class Car : Entity, IAggregateRoot
    {

        public string RegistrationNumber { get; set; }
        public Distance CurrentDistance { get; set; }
        public Distance TotalDistance { get; set; }
        public Position CurrentPosition { get; set; }
        public CarStatus Status { get; set; }
        public Money UnitPrice { get; set; }
        public Car()
        {
        }
        public Car(long carId, string registrationNumber, Distance currentDistance, Distance totalDistance,
            Position currentPosition, CarStatus status, Money unitPrice) : base(carId)
        {
            RegistrationNumber = registrationNumber;
            CurrentDistance = currentDistance;
            TotalDistance = totalDistance;
            CurrentPosition = currentPosition;
            Status = status;
            UnitPrice = unitPrice;
        }

        public void RentalCar()
        {
            if (this.Status != CarStatus.Free)
                throw new Exception($"Car '{this.RegistrationNumber}' is not free.");

            this.Status = CarStatus.Rented;
        }
        public void ReturnCar()
        {
            this.Status = CarStatus.Free;
        }
        public Position GetPosition()
        {
            return this.CurrentPosition;
        }
        public void UpdatePosition(Position p)
        {
            this.CurrentPosition = p;
        }
        public void UpdateTotalDistance(Distance d)
        {
            if (d.Unit == this.TotalDistance.Unit)
                this.TotalDistance.Value += d.Value;
            else
                throw new Exception($"Units are not the same.");
        }

    }

}
