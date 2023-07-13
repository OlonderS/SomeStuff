using Dapper;
using DDD.CarRental.Core.ApplicationLayer.DTOs;
using DDD.CarRental.Core.ApplicationLayer.Mappers;
using DDD.CarRental.Core.DomainModelLayer.Models;
using DDD.CarRental.Core.InfrastructureLayer.EF;
using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;

namespace DDD.CarRental.Core.ApplicationLayer.Queries.Handlers
{
    public class QueryHandler
    {
        private CarRentalDbContext _dbContext;
        private Mapper _mapper;

        public QueryHandler(CarRentalDbContext context, Mapper mapper)
        {
            _dbContext = context;
            _mapper = mapper;
        }

        public List<DriverDto> Execute(GetAllDriversQuery query)
        {
            var drivers = _dbContext.Drivers
                .AsNoTracking()
                .ToList();


            List<DriverDto> result = drivers.Select(r => this._mapper.Map(r)).ToList();

            return result;
        }

        public List<CarDto> Execute(GetAllCarsWithCurrentPositionQuery query)
        {
            var cars = _dbContext.Cars
                .AsNoTracking()
                .Include(r => r.CurrentPosition)
                .Include(r => r.CurrentDistance)
                .Include(r => r.TotalDistance)
                .ToList();

            List<CarDto> result = cars.Select(r => this._mapper.Map(r)).ToList();

            return result;
        }

        public List<RentalDto> Execute(GetAllRentalsQuery query)
        {
            var rentals = _dbContext.Rentals
                .AsNoTracking()
                .Include(r => r.Total)
                .ToList();

            List<RentalDto> result = rentals.Select(r => this._mapper.Map(r)).ToList();

            return result;

        }


        public DriverDto Execute(GetDriverQuery query)
        {
            Driver driver = _dbContext.Drivers
                .AsNoTracking()
                .Where(r => r.Id == query.DriverId)
                .FirstOrDefault();

            if (driver == null)
                throw new Exception($"Could not find driver '{query.DriverId}'");

            DriverDto result = this._mapper.Map(driver);

            return result;

        }

        public CarDto Execute(GetCarQuery query)
        {
            Car car = _dbContext.Cars
                .AsNoTracking()
                .Include(r => r.CurrentPosition)
                .Include(r => r.CurrentDistance)
                .Include(r => r.TotalDistance)
                .Where(r => r.Id == query.CarId)
                .FirstOrDefault();

            if (car== null)
                throw new Exception($"Could not find car '{query.CarId}'");

            CarDto result = this._mapper.Map(car);

            return result;
        }

        public RentalDto Execute(GetRentalQuery query)
        {

            var rental = _dbContext.Rentals
                .AsNoTracking()
                .Include(r => r.Total)
                .Where(r => r.Id == query.RentalId)
                .FirstOrDefault();

            if (rental == null)
                throw new Exception($"Could not find rental '{query.RentalId}'");

            RentalDto result = this._mapper.Map(rental);

            return result;
        
        }
    }
}
