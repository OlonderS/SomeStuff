using DDD.CarRental.Core.ApplicationLayer.DTOs;
using DDD.CarRental.Core.ApplicationLayer.Queries;
using DDD.CarRental.Core.DomainModelLayer.Models;
using System;
using System.Collections.Generic;
using System.Numerics;
using System.Text;

namespace DDD.CarRental.Core.ApplicationLayer.Mappers
{
    public class Mapper
    {
        public RentalDto Map(Rental r)
        {
            return new RentalDto()
            {
                RentalId = r.Id,
                Started = r.Started,
                Finished = r.Finished,
                TimeInHours = r.TimeInHours,
                Total = r.Total,
                CarId = r.CarId,
                DriverId = r.DriverId,
            };
        }

        public DriverDto Map(Driver d)
        {
            return new DriverDto()
            {
                DriverId = d.Id,
                LicenseNumber = d.LicenseNumber,
                FirstName = d.FirstName,
                LastName = d.LastName,
                FreeHours = d.FreeHours

            };
        }

        public CarDto Map(Car c)
        {
            return new CarDto()
            {
                CarId = c.Id,
                RegistrationNumber = c.RegistrationNumber,
                CurrentDistance = Map(c.CurrentDistance),
                TotalDistance = Map(c.TotalDistance),
                CurrentPosition = Map(c.CurrentPosition),
                Status = (CarStatusDto)c.Status,
                UnitPrice = c.UnitPrice

            };
        }
        public PositionDto Map(Position p)
        {
            return new PositionDto()
            {
                X= p.X,
                Y = p.Y,
                Unit = p.Unit
            };
        }

        public DistanceDto Map(Distance d)
        {
            return new DistanceDto()
            {
                Value = d.Value,
                Unit = d.Unit
            };
        }
    }



}
