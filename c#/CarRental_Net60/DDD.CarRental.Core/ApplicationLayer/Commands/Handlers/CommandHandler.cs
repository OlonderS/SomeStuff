using DDD.CarRental.Core.DomainModelLayer.Factories;
using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.CarRental.Core.DomainModelLayer.Models;
using DDD.SharedKernel.DomainModelLayer.Implementations;
using DDD.SharedKernel.InfrastructureLayer;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Numerics;
using System.Text;
using static Microsoft.EntityFrameworkCore.DbLoggerCategory.Database;

namespace DDD.CarRental.Core.ApplicationLayer.Commands.Handlers
{
    public class CommandHandler
    {
        private ICarRentalUnitOfWork _unitOfWork;
        private RentalFactory _rentalFactory;
        private DiscountPolicyFactory _discountPolicyFactory;

        public CommandHandler(ICarRentalUnitOfWork unitOfWork, RentalFactory rentalFactory, DiscountPolicyFactory discountPolicyFactory)
        {
            _unitOfWork = unitOfWork;
            _rentalFactory = rentalFactory;
            _discountPolicyFactory = discountPolicyFactory;

        }

        // funkcja do zapisywania delivery

      
        public void Execute(CreateDriverCommand command)
        {
            Driver driver = this._unitOfWork.DriverRepository.Get(command.DriverId);
            if (driver != null)
                throw new Exception($"Player '{command.DriverId}' already exists.");

            //driver = this._unitOfWork.DriverRepository.GetDriverByLicenseNumber(command.LicenseNumber);


            driver = new Driver(command.DriverId, command.LicenseNumber, command.FirstName, command.LastName, command.FreeHours);
            this._unitOfWork.DriverRepository.Insert(driver);
            this._unitOfWork.Commit();
        }
        
        public void Execute(CreateCarCommand command)
        {
            Car car = new Car(command.CarId, command.RegistrationNumber, command.CurrentDistance, command.TotalDistance,
                command.CurrentPosition, CarStatus.Free, command.UnitPrice);

            this._unitOfWork.CarRepository.Insert(car);
            this._unitOfWork.Commit();
        }
        public void Execute(StartRentalCommand command)
        {

            Car car = this._unitOfWork.CarRepository.Get(command.CarId)
                ?? throw new Exception($"Could not find car '{command.CarId}'."); 
            Driver driver = this._unitOfWork.DriverRepository.Get(command.DriverId)
                ?? throw new Exception($"Could not find driver '{command.DriverId}'.");

            Rental rent = this._rentalFactory.Create(command.RentalId, command.Started, car, driver);

            IDiscountPolicy policy = this._discountPolicyFactory.Create(driver);
            rent.RegisterPolicy(policy);
            car.RentalCar();

            this._unitOfWork.RentalRepository.Insert(rent);
            this._unitOfWork.Commit();
        }
        //DODANIE FUNKCJI DOSTAWY SAMOCHODU
        public void Execute(AddCarDeliveryCommand command)
        {
            CarDelivery delivery = new CarDelivery(command.RentalId, command.Distance, command.DateTime);
            this._unitOfWork.CarDeliveryRepository.Insert(delivery);
            this._unitOfWork.Commit();
             
            Rental renatalWithDelivery = this._unitOfWork.RentalRepository.Get(command.RentalId);
            Car carWithDelivery = this._unitOfWork.CarRepository.Get(renatalWithDelivery.CarId);
            renatalWithDelivery.DeliveryPrice = new Money(command.Distance.GetDistanceInKilometers() * carWithDelivery.UnitPrice.Amount); // mozna zmienic cene tak zeby nie byly takie kosmiczne
            this._unitOfWork.Commit();
        }
        public void Execute(StopRentalCommand command)
        {
            Rental rental = this._unitOfWork.RentalRepository.Get(command.RentalId)
                ?? throw new Exception($"Could not find rental '{command.RentalId}'.");
            Car car = this._unitOfWork.CarRepository.Get(rental.CarId)
                ?? throw new Exception($"Could not find car '{rental.CarId}'.");
            Driver driver = this._unitOfWork.DriverRepository.Get(rental.DriverId)
                ?? throw new Exception($"Could not find driver '{rental.DriverId}'.");


            car.ReturnCar();
            Position newPos = car.GetPosition();
            car.UpdatePosition(newPos);


            int FreeHours = rental.StopRentalCommand(command.Finished, car.UnitPrice, driver.FreeHours);
            driver.UpdateFreeHours(FreeHours);

            this._unitOfWork.Commit();
        }

    }
}
