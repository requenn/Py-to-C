#ifndef OBJECT_H
#define OBJECT_H

#include <stdio.h>
#include <stdbool.h>

// Метки типов данных
typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_BOOL
} TypeTag;

// Универсальный объект (значение + тип)
typedef struct {
    TypeTag type;
    union {
        long long int_val;
        double float_val;
        bool bool_val;
    } data;
} object_t;

// Конструкторы базовых значений
object_t* INT(long long v);
object_t* FLOAT(double v);
object_t* TRUE(void);
object_t* FALSE(void);

// Арифметические функции
object_t* ADD(object_t* a, object_t* b);
object_t* SUB(object_t* a, object_t* b);
object_t* MUL(object_t* a, object_t* b);
object_t* DIV(object_t* a, object_t* b);
object_t* POW_OP(object_t* a, object_t* b);

// Печать объекта в консоль
void print_object(object_t* obj);

#endif 