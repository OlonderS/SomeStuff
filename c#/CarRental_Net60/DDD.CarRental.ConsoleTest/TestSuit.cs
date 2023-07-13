using DDD.CarRental.Core.ApplicationLayer.Commands;
using DDD.CarRental.Core.ApplicationLayer.Commands.Handlers;
using DDD.CarRental.Core.ApplicationLayer.Queries;
using DDD.CarRental.Core.ApplicationLayer.Queries.Handlers;
using DDD.CarRental.Core.DomainModelLayer.Models;
using DDD.SharedKernel.DomainModelLayer.Implementations;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Runtime.ConstrainedExecution;
using System.Text;

namespace DDD.CarRental.ConsoleTest
{
    public class TestSuit
    {
        private IServiceProvider _serviceProvide;

        private CommandHandler _commandHandler;
        private QueryHandler _queryHandler;

        public TestSuit(IServiceCollection serviceCollection)
        {
            _serviceProvide = serviceCollection.BuildServiceProvider();

            _commandHandler = _serviceProvide.GetRequiredService<CommandHandler>();
            _queryHandler = _serviceProvide.GetRequiredService<QueryHandler>();
        }

        public void Run()
        {
            long car1Id = 11;
            long car2Id = 12;
            long driver1Id = 21;
            long driver2Id = 22;
            long rental1Id = 31;
            long rental2Id = 32;
            long deliveryId = 1;

            // tworzymy samochód
            _commandHandler.Execute(new CreateCarCommand()
            {
                CarId = car1Id,
                RegistrationNumber = "KR123456",
                CurrentDistance = new Distance(100, UnitDistanceEnum.Kilometers),
                TotalDistance = new Distance(1000, UnitDistanceEnum.Kilometers),
                CurrentPosition = new Position(car1Id, "KR123456", 50.0614300m, 19.9365800m, UnitPositionEnum.Degrees),
                UnitPrice = new Money(20)
            });

            _commandHandler.Execute(new CreateCarCommand()
            {
                CarId = car2Id,
                RegistrationNumber = "WA123123",
                CurrentDistance = new Distance(250, UnitDistanceEnum.Miles),
                TotalDistance = new Distance(12200, UnitDistanceEnum.Miles),
                CurrentPosition = new Position(car2Id, "WA123123", 50.1914300m, 17.9365800m, UnitPositionEnum.Degrees),
                UnitPrice = new Money(20)
            });

            // pobieramy info o autach
            Console.WriteLine("Utworzono auto");
            var cars = _queryHandler.Execute(new GetAllCarsWithCurrentPositionQuery());
            foreach (var car in cars)
            {
                Console.WriteLine($"Id pokoju: {car.CarId}, Number rejestracji: {car.RegistrationNumber}, Aktualna odległość: {car.CurrentDistance.Value} {car.CurrentDistance.Unit}  " +
                    $"Całkowity przebieg: {car.TotalDistance.Value} {car.TotalDistance.Unit}  , Aktualna pozycja(X; Y): {car.CurrentPosition.X}; {car.CurrentPosition.Y}");
            }


            // tworzymy 2 kierowców
            _commandHandler.Execute(new CreateDriverCommand()
            {
                DriverId = driver1Id,
                LicenseNumber = "123",
                FirstName = "Janina",
                LastName = "Kowalska",
                FreeHours = 5
            });

            _commandHandler.Execute(new CreateDriverCommand()
            {
                DriverId = driver2Id,
                LicenseNumber = "8900",
                FirstName = "Janusz",
                LastName = "Nowak",
                FreeHours = 0
            });

            // pobieramy info o kierowcach
            Console.WriteLine("Utworzono dwóch kierowców");
            var drivers = _queryHandler.Execute(new GetAllDriversQuery());
            foreach (var driver in drivers)
            {
                Console.WriteLine($"Id kierowcy: {driver.DriverId}, Numer licencji: {driver.LicenseNumber}, Imię: {driver.FirstName}, " +
                    $"Nazwisko: {driver.LastName}, Liczba wolnych godzin: {driver.FreeHours}");
            }

            // kierowca 1 wypożycza samochód
            _commandHandler.Execute(new StartRentalCommand()
            {
                RentalId = rental1Id,
                Started = new DateTime().AddHours(1).AddMinutes(0),
                CarId = car1Id,
                DriverId = driver1Id
            });

            // pobieramy info o wypożyczeniach
            Console.WriteLine("\nKierowca 1 wypożycza samochód");
            var rentals = _queryHandler.Execute(new GetAllRentalsQuery());
            foreach (var rental in rentals)
            {
                Console.WriteLine($"Id wypożyczenia: {rental.RentalId}, Id kierowcy: {rental.DriverId}, " +
                    $"Id Samochodu: {rental.CarId}, Rozpoczęcie: {rental.Started}, Zakończenie: {rental.Finished}, " +
                    $"Czas: {rental.TimeInHours}h, Cena: {rental.Total.Amount} {rental.Total.Currency}");
            }

            // kierowca 1 kończy wypożyczenie
            _commandHandler.Execute(new StopRentalCommand()
            {
                RentalId = rental1Id,
                Finished = new DateTime().AddHours(100).AddMinutes(0)
            });

            // pobieramy info o wypożyczeniach
            Console.WriteLine("\nKierowca 1 kończy wypożyczać samochód");
            rentals = _queryHandler.Execute(new GetAllRentalsQuery());
            foreach (var rental in rentals)
            {
                Console.WriteLine($"Id wypożyczenia: {rental.RentalId}, Id kierowcy: {rental.DriverId}, " +
                    $"Id Samochodu: {rental.CarId}, Rozpoczęcie: {rental.Started}, Zakończenie: {rental.Finished}, " +
                    $"Czas: {rental.TimeInHours}h, Cena: {rental.Total.Amount} {rental.Total.Currency}");
            }


        // kierowca 2 wypożycza samochód
        _commandHandler.Execute(new StartRentalCommand()
            {
                RentalId = rental2Id,
                Started = new DateTime().AddHours(0).AddMinutes(30),
                CarId = car2Id,
                DriverId = driver2Id
            });

            // pobieramy info o wypożyczeniach
            Console.WriteLine("\nKierowca 2 wypożycza samochód");
            rentals = _queryHandler.Execute(new GetAllRentalsQuery());
            foreach (var rental in rentals)
            {
                Console.WriteLine($"Id wypożyczenia: {rental.RentalId}, Id kierowcy: {rental.DriverId}, " +
                    $"Id Samochodu: {rental.CarId}, Rozpoczęcie: {rental.Started}, Zakończenie: {rental.Finished}, " +
                    $"Czas: {rental.TimeInHours}h, Cena: {rental.Total.Amount} {rental.Total.Currency} ");
            }


            Console.WriteLine("dostawa: ");
            // dodajemy dostawę do wypożyczenia 32
            _commandHandler.Execute(new AddCarDeliveryCommand()
            {
                RentalId = rental2Id,
                Distance = new Distance(100, UnitDistanceEnum.Miles),
                DateTime = new DateTime().AddHours(5)
            });

            Console.WriteLine($"Id : {rental2Id}, odległość dostawy: {100} {UnitDistanceEnum.Miles.ToString().ToLower()}");

            // kierowca 2 kończy wypożyczać
            _commandHandler.Execute(new StopRentalCommand()
            {
                RentalId = rental2Id,
                Finished = new DateTime().AddHours(52).AddMinutes(30)
            });

            // pobieramy info o wypożyczeniach
            Console.WriteLine("\nKierowca 2 kończy wypożyczać samochód");
            rentals = _queryHandler.Execute(new GetAllRentalsQuery());
            foreach (var rental in rentals)
            {
                Console.WriteLine($"Id wypożyczenia: {rental.RentalId}, Id kierowcy: {rental.DriverId}, " +
                    $"Id Samochodu: {rental.CarId}, Rozpoczęcie: {rental.Started}, Zakończenie: {rental.Finished}, " +
                    $"Czas: {rental.TimeInHours}h, Cena: {rental.Total.Amount} {rental.Total.Currency}");
            }
            

            // pobieramy info o wypożyczeniu 31
            Console.WriteLine("\nWypozyczenie 31:");
            var rental31 = _queryHandler.Execute(new GetRentalQuery() { RentalId = 31 });
     

            Console.WriteLine($"Id wypożyczenia: {rental31.RentalId}, Id kierowcy: {rental31.DriverId}, " +
            $"Id Samochodu: {rental31.CarId}, Rozpoczęcie: {rental31.Started}, Zakończenie: {rental31.Finished}, " +
            $"Czas: {rental31.TimeInHours}h, Cena: {rental31.Total.Amount} {rental31.Total.Currency}");

            // pobieramy info o aucie 11
            Console.WriteLine("\nAuto 11:");
            var car11 = _queryHandler.Execute(new GetCarQuery() { CarId = 11 });
            Console.WriteLine($"Id samochodu: {car11.CarId}, Numer rejestracji: {car11.RegistrationNumber}, Aktualna odległość: {car11.CurrentDistance.Value} {car11.CurrentDistance.Unit}  " +
            $"Całkowity przebieg: {car11.TotalDistance.Value} {car11.TotalDistance.Unit}  , Aktualna pozycja(X; Y): {car11.CurrentPosition.X}; {car11.CurrentPosition.Y}");


            // pobieramy info o kierowcy 21
            Console.WriteLine("\nKierowca 21:");
            var driver21 = _queryHandler.Execute(new GetDriverQuery() { DriverId = 21 });
            Console.WriteLine($"Id kierowcy: {driver21.DriverId}, Numer licencji: {driver21.LicenseNumber}, Imię: {driver21.FirstName}, " +
            $"Nazwisko: {driver21.LastName}, Liczba wolnych godzin: {driver21.FreeHours}");
            

        }
    }
}
