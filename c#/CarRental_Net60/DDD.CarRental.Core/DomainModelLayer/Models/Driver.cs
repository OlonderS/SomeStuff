using DDD.SharedKernel.DomainModelLayer;
using DDD.SharedKernel.DomainModelLayer.Implementations;
using System.Xml.Linq;
using System;

namespace DDD.CarRental.Core.DomainModelLayer.Models
{
    public class Driver : Entity, IAggregateRoot
    {
        public string LicenseNumber { get; protected set; }
        public string FirstName { get; protected set; }
        public string LastName { get; protected set; }
        public int FreeHours { get; protected set; }

        public Driver()
        {
        }
        public Driver(long driverId, string licenseNumber, string firstName, 
            string lastName, int freeHours ) : base(driverId)
        {
            if (String.IsNullOrEmpty(licenseNumber)) throw new Exception("Licence number is null or empty");
            if (String.IsNullOrEmpty(firstName)) throw new Exception("First name is null or empty");
            if (String.IsNullOrEmpty(lastName)) throw new Exception("Last name is null or empty");
            if (String.IsNullOrEmpty(freeHours.ToString())) throw new Exception("Free minutes is null or empty");

            LicenseNumber = licenseNumber;
            FirstName = firstName;
            LastName = lastName;
            FreeHours = freeHours;

            //this.AddDomainEvent(new DriverCreatedDomainEvent(this.Id, this.LicenceNumber, this.FirstName, this.LastName, this.FreeMinutes));

        }

        public void UpdateFreeHours(int freeHours)
        {
            FreeHours = freeHours;
        }
    }

}
