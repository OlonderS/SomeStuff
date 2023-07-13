using DDD.SharedKernel.InfrastructureLayer;
using System;

namespace DDD.CarRental.Core.DomainModelLayer.Interfaces
{
    public interface ICarRentalUnitOfWork : IUnitOfWork, IDisposable
    {
        ICarRepository CarRepository { get; }
        IDriverRepository DriverRepository { get; }
        IRentalRepository RentalRepository { get; }
        ICarDeliveryRepository CarDeliveryRepository { get; }
    }
}
