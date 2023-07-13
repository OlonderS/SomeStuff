using DDD.CarRental.Core.DomainModelLayer.Events;
using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.SharedKernel.DomainModelLayer;
using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Text;

namespace DDD.CarRental.Core.DomainModelLayer.Models
{
    public class Rental : Entity, IAggregateRoot
    {
        public DateTime Started { get; protected set; }
        public DateTime? Finished { get; protected set; }
        public int TimeInHours { get; set; }
        public Money Total { get; protected set; }
        public long CarId { get; protected set; }
        public long DriverId { get; protected set; }

        private IDiscountPolicy _policy;

        public Money DeliveryPrice = Money.Zero;


        public Rental()
        {
        }

        public Rental(long rentalId, long carId, long driverId, DateTime started) : base(rentalId)
        {
            this.Started= started;
            this.CarId= carId;
            this.DriverId= driverId;
            this.Total = Money.Zero;

            this.AddDomainEvent(new RentalStartedDomainEvent(this));

        }

        

        public void RegisterPolicy(IDiscountPolicy policy)
        {
            this._policy = policy ?? throw new ArgumentNullException("Empty discount policy");
        }
        public int StopRentalCommand(DateTime finished, Money unitPrice, int FreeHours)
        {
            if (finished < Started)
                throw new Exception($"Rental return date and time is earlier than enter date and time.");

            Finished = finished;

            TimeInHours = GetTimeInHours() - FreeHours;
            Total = unitPrice.MultiplyBy(this.TimeInHours);


            if (this._policy != null)
            {
                (Money discount, int freeHours) = this._policy.CalculateDiscount(this.Total, this.TimeInHours, unitPrice);
                Total = (discount > Total) ? Money.Zero : Total - discount;
                FreeHours = freeHours;
            }

            Total += DeliveryPrice;

            // publish event
            this.AddDomainEvent(new RentalFishedDomainEvent(this));
            return FreeHours;
        }
        public int GetTimeInHours()
        {
            if (!this.Finished.HasValue) return 0;
            return (int)(this.Finished.Value - this.Started).TotalHours;
        }
    }

}
