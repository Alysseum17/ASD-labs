#include <stdio.h>
#include <stdlib.h>
typedef struct linked_list {
    double data;
    struct linked_list *next_p;
}l_list;
l_list *init_list(double data){
    l_list *last_node = malloc(sizeof(l_list));
    /*
    *last_node = (linked_list){
        .data = data,
        .next_p = NULL
    };
    */
    // Easier way
    last_node -> data = data;
    last_node->next_p = NULL;
    return last_node;
}
l_list *add_node(l_list *last_node, double data){
    l_list *new_node = malloc(sizeof(l_list));
    new_node->data = data;
    new_node->next_p = last_node;
    return new_node;
}
void print_list(l_list *last_node){
    l_list *current_node = last_node;
    while(current_node){
        printf("Element = %lf \n",current_node->data);
        current_node = current_node->next_p;
    }
}
void free_memory(l_list *last_node){
    l_list *current_node;
    while(last_node){
        current_node = last_node;
        last_node = last_node -> next_p;
        free(current_node);
    }
}
 int isNonIncreasing(l_list *last_node){
    if(last_node == NULL || last_node->next_p == NULL){
        printf("List with 0 or 1 element always not increasing\n");
        return 1;
    }
    l_list *current_node = last_node;
    while(current_node->next_p){
        if(current_node->data < current_node->next_p->data){
            printf("The list is sorted in increasing order\n");
            return 0;
        }
        current_node = current_node->next_p;
    }
    printf("The list is sorted in not increasing order\n");
    return 1;
}
l_list *reverse_list(l_list *last_node){
    l_list *prev_node = NULL;
    l_list *current_node = last_node;
    l_list *next_node = NULL;
    while(current_node){
        next_node = current_node->next_p;
        current_node->next_p = prev_node;
        prev_node = current_node;
        current_node = next_node;
    }
    return prev_node;
}
int main()
{
    size_t result_node;
    int n;
    double value;
    printf("Enter the number of nodes in the list: \n");
    scanf("%d",&n);
    for(unsigned int i = 0; i < n; i++){
        if(i==0){
            printf("Enter a value of node: \n");
            scanf("%lf", &value);
            result_node = init_list(value);
        }else{
            printf("Enter a value of node: \n");
            scanf("%lf", &value);
            result_node = add_node(result_node, value);
        }
    }
    print_list(result_node);
    if(!isNonIncreasing(result_node)){
       result_node = reverse_list(result_node);
        print_list(result_node);
    }
    return 0;
}