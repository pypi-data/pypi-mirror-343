def experiment5():
    """Run NLP Text Analysis"""
    from .experiment5 import run
    run()

def experiment6():
    """Run Tree Visualizer"""
    from .experiment6 import run
    run()

def experiment7():
    """Run Graph Visualizer"""
    from .experiment7 import run
    run()

def experiment8():
    """Run Clustering Demo"""
    from .experiment8 import run
    run()

def main():
    print("🏹 Archer Queen CLI 🏹")
    print("Available experiments:")
    print("1. NLP Text Analysis")
    print("2. Tree Visualizer")
    print("3. Graph Visualizer")
    print("4. Clustering Demo")
    
    choice = input("Enter experiment number (1-4): ")
    {
        '1': experiment5,
        '2': experiment6,
        '3': experiment7,
        '4': experiment8
    }.get(choice, lambda: print("Invalid choice!"))()

if __name__ == "__main__":
    main()