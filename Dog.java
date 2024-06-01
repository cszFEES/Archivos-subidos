public class Dog {
    String name;
    int age;

    public Dog(String name, int age) {
        this.name = name;
        this.age = age;
    }


    public static void main(String[] args) {
        Dog myDog = new Dog("canis naturalis",4);
        System.out.println(myDog.name);
        System.out.println(myDog.age);
    }
}