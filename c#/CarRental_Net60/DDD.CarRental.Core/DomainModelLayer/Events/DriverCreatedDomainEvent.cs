
using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Collections.Generic;
using System.Text;

namespace DDD.CarRental.Core.DomainModelLayer.Events
{
    public class DriverCreatedDomainEvent : DomainEvent
    {
        public long DriverId { get; set; }
        public string LicenseNumber { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public decimal FreeHours { get; set; }

        public DriverCreatedDomainEvent(long driverId, string licenseNumber, string firstName, string lastName, decimal freeHours)
        {
            this.DriverId = driverId;
            this.LicenseNumber = licenseNumber;
            this.FirstName = firstName;
            this.LastName = lastName;
            this.FreeHours = freeHours;
        }         

    }
}
