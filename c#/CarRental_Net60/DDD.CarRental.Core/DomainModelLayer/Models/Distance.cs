using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Collections.Generic;

namespace DDD.CarRental.Core.DomainModelLayer.Models
{    
    // Dodanie Enum dla jednostki
    public enum UnitDistanceEnum
    {
        Kilometers,
        Miles
            
    }

    public class Distance : ValueObject
    { 
        //public string Car { get; set; }
        public decimal Value { get; set; }

        public UnitDistanceEnum Unit { get; set; }
        public static Distance Zero = new Distance()
        {
            Value = 0,
            Unit = UnitDistanceEnum.Kilometers,
        };
        protected Distance()
        { }

        public Distance(/*long carId,*/ /*string registrationNumber,*/ decimal value, UnitDistanceEnum unit)
        {
            //Car = "CarId: " + carId + " (" + registrationNumber + ")";
            Value = value;
            Unit = unit;
        }

        protected override IEnumerable<object> GetEqualityComponents()
        {
            //yield return Car.ToUpper();
            yield return Value;
            yield return Unit;
        }

        // Przeliczanie Mil na km i odwrotnie
        public decimal GetDistanceInKilometers()
        {
           return  this.Unit == UnitDistanceEnum.Kilometers ? this.Value : this.Value * (decimal)1.6093;
        }

        public decimal GetDistanceInMiles() 
        {
            return this.Unit == UnitDistanceEnum.Miles ? this.Value : this.Value / (decimal)1.6093;
        }

        // Operatory Porównania
        public int Compare(Distance d)
        {
            //return this.TimeInMinutes.CompareTo(s.TimeInMinutes);
            return this.GetDistanceInKilometers().CompareTo(d.GetDistanceInKilometers());
        }

        public static bool operator <(Distance d1, Distance d2)
        {
            //return m.TimeInMinutes.CompareTo(m2.TimeInMinutes) < 0;
            return d1.GetDistanceInKilometers().CompareTo(d2.GetDistanceInKilometers()) < 0;
        }

        public static bool operator >(Distance d1, Distance d2)
        {
            //return m.TimeInMinutes.CompareTo(m2.TimeInMinutes) > 0;
            return d1.GetDistanceInKilometers().CompareTo(d2.GetDistanceInKilometers()) > 0;
        }

        public static bool operator >=(Distance d1, Distance d2)
        {
            return d1.GetDistanceInKilometers().CompareTo(d2.GetDistanceInKilometers()) >= 0;
        }

        public static bool operator <=(Distance d1, Distance d2)
        {
            return d1.GetDistanceInKilometers().CompareTo(d2.GetDistanceInKilometers()) <= 0;
        }


    }

}
