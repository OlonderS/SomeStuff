using DDD.CarRental.Core.DomainModelLayer.Models;
using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.ApplicationLayer.DTOs
{
    public enum CarStatusDto
    {
        Free = 0,
        Reserved = 1,
        Rented = 2
    }

    public class CarDto
    {
        public long CarId;
        public string RegistrationNumber { get; set; }
        public DistanceDto CurrentDistance { get; set; }
        public DistanceDto TotalDistance { get; set; }
        public PositionDto CurrentPosition { get; set; }
        public CarStatusDto Status { get; set; }
        public Money UnitPrice { get; set; }
    }

}
