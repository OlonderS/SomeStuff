
using DDD.SharedKernel.DomainModelLayer.Implementations;

namespace DDD.CarRental.Core.DomainModelLayer.Interfaces
{
    public interface IDiscountPolicy
    {
        string Name { get; }
        (Money, int) CalculateDiscount(Money total, int numOfHours, Money unitPrice);
    }
}