
def main():
    path = ['a','b','c','a','e','b']
    dict={}
    for i in path:
        if(i in dict):
            dict[i] = dict[i]+1;
        else:
            dict[i]=1;
    print(dict)

if __name__ == '__main__':
    main()