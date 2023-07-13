using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Collections.Generic;

namespace DDD.CarRental.Core.DomainModelLayer.Models
{    
    // enum dla stopni i minut
    public enum UnitPositionEnum
       {
         Degrees,
         Minutes
       }
    public class Position : ValueObject
    {
        public string Car { get; protected set; }
        public decimal X { get; protected set; }
        public decimal Y { get; protected set; }
        public UnitPositionEnum Unit { get; protected set; }

        protected Position()
        { }

        public Position(long carId, string registrationNumber, decimal x, decimal y, UnitPositionEnum unit)
        {
            Car = "CarId: " + carId + " (" + registrationNumber + ")";
            X = x;
            Y = y;
            Unit = unit;

        }

        protected override IEnumerable<object> GetEqualityComponents()
        {
            yield return Car.ToUpper();
            yield return X;
            yield return Y;
        }

        
        // zwroc dystans w kilometrach
        public Distance CalculateDistanceInKilometers(Position position)
        {
            decimal XKilometersThis;
            decimal YKilometersThis;
            decimal XKilometersCompared;
            decimal YKilometersCompared;

            // zamiania na minuty wszystkiego
            if(this.Unit == UnitPositionEnum.Degrees)
            {
                XKilometersThis = 60 * this.X * (decimal)1.85;
                YKilometersThis = 60 * this.Y * (decimal)1.85;
            }
            else
            {
                XKilometersThis = X * (decimal)1.85;
                YKilometersThis = Y * (decimal)1.85;
            }

            if(position.Unit == UnitPositionEnum.Degrees)
            {
                XKilometersCompared = position.X * 60 * (decimal)1.85;
                YKilometersCompared = position.Y * 60 * (decimal)1.85;
            }
            else
            {
                XKilometersCompared = position.X * (decimal)1.85;
                YKilometersCompared = position.Y * (decimal)1.85;
            }

            decimal dis = (decimal)Math.Sqrt(
           Math.Pow(((double)XKilometersThis - (double)XKilometersCompared), 2)
           + Math.Pow(((double)XKilometersThis - (double)XKilometersCompared), 2));

            Distance distance = new Distance(dis, UnitDistanceEnum.Kilometers);
            return distance;
            
        }
    }

}
