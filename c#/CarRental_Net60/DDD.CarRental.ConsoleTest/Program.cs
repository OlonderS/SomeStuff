using DDD.CarRental.Core.ApplicationLayer.Commands.Handlers;
using DDD.CarRental.Core.ApplicationLayer.Mappers;
using DDD.CarRental.Core.ApplicationLayer.Queries.Handlers;
using DDD.CarRental.Core.DomainModelLayer.Factories;
using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.CarRental.Core.InfrastructureLayer.EF;
using DDD.SharedKernel.DomainModelLayer;
using DDD.SharedKernel.InfrastructureLayer.Implementations;
using Microsoft.Extensions.DependencyInjection;
using System;

namespace DDD.CarRental.ConsoleTest
{
    class Program
    {
        static void Main(string[] args)
        {
            // create and configure DI container
            IServiceCollection serviceCollection = new ServiceCollection();
            ConfigureServices(serviceCollection);

            // create TestSuit & run scenario test
            var testSuit = new TestSuit(serviceCollection);
            testSuit.Run();
        }

        static private void ConfigureServices(IServiceCollection serviceCollection)
        {
            // intializing and registering CarRentalDbContext
            var context = TestUtils.InitializeCarRentalContext();
            serviceCollection.AddSingleton(context);

            // registering command and query handlers
            serviceCollection.AddSingleton<CommandHandler>();
            serviceCollection.AddSingleton<QueryHandler>();

            // registering event publisher and handlers
            serviceCollection.AddSingleton<IDomainEventPublisher, SimpleEventPublisher>();
            
            // registering unit of work and repos
            serviceCollection.AddSingleton<ICarRentalUnitOfWork, CarRentalUnitOfWork>();
            serviceCollection.AddSingleton<ICarRepository, CarRepository>();
            serviceCollection.AddSingleton<IDriverRepository, DriverRepository>();
            serviceCollection.AddSingleton<IRentalRepository, RentalRepository>();
            //DODANIE Dependency Injection dla carDeliveryRepository
            serviceCollection.AddSingleton<ICarDeliveryRepository, CarDeliveryRepository>();
            
            // registering domain model services, factories
            serviceCollection.AddSingleton<Mapper>();
            serviceCollection.AddSingleton<RentalFactory>();
            serviceCollection.AddSingleton<DiscountPolicyFactory>();
            // ToDo: Zarejestruj pozostałe usługi, fabryki, polityki, itp.
        }
    }
}
