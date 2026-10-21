#include "object.h"
#include <stdlib.h>
#include <math.h>

// Создание целого числа
object_t* INT(long long v) {
    object_t* obj = (object_t*)malloc(sizeof(object_t));
    obj->type = TYPE_INT;
    obj->data.int_val = v;
    return obj;
}

// Создание дробного числа
object_t* FLOAT(double v) {
    object_t* obj = (object_t*)malloc(sizeof(object_t));
    obj->type = TYPE_FLOAT;
    obj->data.float_val = v;
    return obj;
}

// Создание True
object_t* TRUE(void) {
    object_t* obj = (object_t*)malloc(sizeof(object_t));
    obj->type = TYPE_BOOL;
    obj->data.bool_val = true;
    return obj;
}

// Создание False
object_t* FALSE(void) {
    object_t* obj = (object_t*)malloc(sizeof(object_t));
    obj->type = TYPE_BOOL;
    obj->data.bool_val = false;
    return obj;
}

// Перевод объекта в double
static double to_double(object_t* obj) {
    if (obj->type == TYPE_FLOAT) {
        return obj->data.float_val;
    }
    if (obj->type == TYPE_INT) {
        return (double)obj->data.int_val;
    }
    if (obj->type == TYPE_BOOL) {
        if (obj->data.bool_val == true) {
            return 1.0;
        }
        else {
            return 0.0;
        }
    }
    return 0.0;
}

// Перевод объекта в целое число
static long long to_int(object_t* obj) {
    if (obj->type == TYPE_INT) {
        return obj->data.int_val;
    }
    if (obj->type == TYPE_BOOL) {
        if (obj->data.bool_val == true) {
            return 1;
        }
        else {
            return 0;
        }
    }
    return (long long)obj->data.float_val;
}

// Сложение
object_t* ADD(object_t* a, object_t* b) {
    if (a->type == TYPE_FLOAT || b->type == TYPE_FLOAT) {
        return FLOAT(to_double(a) + to_double(b));
    }
    return INT(to_int(a) + to_int(b));
}

// Вычитание
object_t* SUB(object_t* a, object_t* b) {
    if (a->type == TYPE_FLOAT || b->type == TYPE_FLOAT) {
        return FLOAT(to_double(a) - to_double(b));
    }
    return INT(to_int(a) - to_int(b));
}

// Умножение
object_t* MUL(object_t* a, object_t* b) {
    if (a->type == TYPE_FLOAT || b->type == TYPE_FLOAT) {
        return FLOAT(to_double(a) * to_double(b));
    }
    return INT(to_int(a) * to_int(b));
}

// Деление
object_t* DIV(object_t* a, object_t* b) {
    return FLOAT(to_double(a) / to_double(b));
}

// Возведение в степень
object_t* POW_OP(object_t* a, object_t* b) {
    double res = pow(to_double(a), to_double(b));
    if (a->type == TYPE_INT && b->type == TYPE_INT && b->data.int_val >= 0) {
        return INT((long long)res);
    }
    return FLOAT(res);
}

// Печать
void print_object(object_t* obj) {
    if (obj->type == TYPE_INT) {
        printf("%lld\n", obj->data.int_val);
    }
    else if (obj->type == TYPE_FLOAT) {
        printf("%g\n", obj->data.float_val);
    }
    else if (obj->type == TYPE_BOOL) {
        if (obj->data.bool_val == true) {
            printf("True\n");
        }
        else {
            printf("False\n");
        }
    }
}