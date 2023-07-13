using DDD.SharedKernel.DomainModelLayer.Implementations;
using System;
using System.Collections.Generic;

namespace DDD.CarRental.Core.DomainModelLayer.Models
{
    public class PositionDto
    {
        public string Car { get; set; }
        public decimal X { get; set; }

        public decimal Y { get; set; }

        public UnitPositionEnum Unit { get; set; }

    }

}

