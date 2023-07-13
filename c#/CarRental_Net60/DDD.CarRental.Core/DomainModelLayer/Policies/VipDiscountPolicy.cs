using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.SharedKernel.DomainModelLayer.Implementations;

namespace DDD.CarRental.Core.DomainModelLayer.Policies
{

    public class VipDiscountPolicy : IDiscountPolicy
    {
        public string Name { get; protected set; }
        public int FreeHours { get; protected set; }
        public VipDiscountPolicy(int freeHours)
        {
            Name = "Vip discount policy";
            FreeHours = freeHours;
        }

        public (Money, int) CalculateDiscount(Money total, int numOfHours, Money unitPrice)
        {
            int timeInHours = numOfHours + FreeHours;
            Money discount = unitPrice.MultiplyBy(FreeHours);
            FreeHours = (FreeHours > timeInHours) ? (FreeHours - timeInHours) : 0;
            FreeHours += (int)(numOfHours * 0.15);
            return (discount, FreeHours); //free hours konkretnego kierowcy poprawic
        }
    }
}
