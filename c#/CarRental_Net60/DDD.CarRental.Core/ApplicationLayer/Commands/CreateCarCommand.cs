using DDD.CarRental.Core.DomainModelLayer.Models;
using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DDD.CarRental.Core.ApplicationLayer.Commands
{
    public enum CarStatusCommand
    {
        Free = 0,
        Reserved = 1,
        Rented = 2
    }

    public class CreateCarCommand
    {
        public long CarId;
        public string RegistrationNumber { get; set; }
        public Distance CurrentDistance { get; set; }
        public Distance TotalDistance { get; set; }
        public Position CurrentPosition { get; set; }
        public CarStatusCommand Status{ get; set; }
        public Money UnitPrice { get; set; }
    }
}
