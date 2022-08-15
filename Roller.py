class Roller():
    def __init__(self):
        pass

    ######################################################################
    # Function: __ListProduct
    #
    # Description:
    #    Build List Product.
    #
    # Parameters:
    #    MainList  - the Main List of dice combination.
    #    ListB     - the dice to add to the combination.
    #
    # Return: 
    #    TupleList - the Tuple List of combination.
    ######################################################################
    def __ListProduct(self, MainList, ListB):
        TupleList = []

        for Ob in MainList:
            for x in ListB:
                TempList = []
                if type(Ob) is tuple or type(Ob) is list:
                    TempList = list(Ob)
                else:
                    TempList.append(Ob)
                TempList.append(x)
                TupleList.append(tuple(TempList))
        return TupleList

    ######################################################################
    # Function: __buildGeneralDice
    #
    # Description:
    #    Build general dice.
    #
    # Parameters:
    #    DiceSize  - the dice size.
    #
    # Return: 
    #    the general dice.
    ######################################################################
    def __buildGeneralDice(self,DiceSize):
        return [i for i in range(1,int(DiceSize)+1)]

    ######################################################################
    # Function: __DiceCombination
    #
    # Description:
    #    Create the Dice Combination.
    #
    # Parameters:
    #    DiceTypeList  - all the dice that need to be included in the combination.
    #
    # Return: 
    #    ComboList - all the dice combination.
    ######################################################################
    def __DiceCombination(self, DiceTypeList):
        ComboList = []
        flage = 1
        for items in DiceTypeList:
            for _ in range(items[0]):
                if flage:
                    flage = 0
                    if 'd' in items[1]:
                        ComboList = self.__buildGeneralDice(items[1][1:len(items[1])])
                    else:
                        ComboList = items[1]
                else:
                    if 'd' in items[1]:
                        Dice = self.__buildGeneralDice(items[1][1:len(items[1])])
                        ComboList = self.__ListProduct(ComboList,Dice)
                    else:
                        ComboList = self.__ListProduct(ComboList,items[1])

        return ComboList

    ######################################################################
    # Function: __PassFuncation
    #
    # Description:
    #    Pass Funcation.
    #
    # Parameters:
    #    Ob  - the object to pass.
    #
    # Return: 
    #    Ob - the object to pass.
    ######################################################################
    def __PassFuncation(self, Ob):
        return Ob

    ######################################################################
    # Function: __FuncRole
    #
    # Description:
    #    chose the relevent funcation to operate on the combination list tuple.
    #
    # Parameters:
    #    ComboListTuple  - the Combo list tuple.
    #    funcStr         - the func name string.
    #
    # Return: 
    #    ValiueDict - the Valiue Dict of the selected funcation.
    ######################################################################
    def __FuncRole(self, ComboListTuple, funcStr):
        if type(ComboListTuple[0]) is not tuple:
            func = self.__PassFuncation
        elif funcStr == "Max":
            func = max
        elif funcStr == "Min":
            func = min
        elif funcStr == "Sum":
            func = sum
        ValiueDict = self.__BuildValiueDict(ComboListTuple, func)
        return ValiueDict

    ######################################################################
    # Function: __BuildValiueDict
    #
    # Description:
    #    Build Valiue Dict.
    #
    # Parameters:
    #    ComboListTuple  - the Combo list tuple.
    #    func  - the function.
    #
    # Return: 
    #    ValiueDict - the Dict of Valiue of the selected funcation.
    ######################################################################
    def __BuildValiueDict(self, ComboListTuple, func):
        UniqueDict = {}
        for item in ComboListTuple:
            if func(item) not in UniqueDict:
                UniqueDict[func(item)] = 1
            else:
                UniqueDict[func(item)] += 1
        return UniqueDict

    def __Unique(self, listOb):
        # initialize a null list
        unique_list = []
        # traverse for all elements
        for item in listOb:
            if type(item) is tuple:
                for tuplItem in item:
                    if tuplItem not in unique_list:
                        unique_list.append(tuplItem)
            # check if exists in unique_list or not
            elif item not in unique_list:
                unique_list.append(item)
        #unique_list.append(max(unique_list)+1)

        return sorted(unique_list)

    def __buildUniqueDict(self, listOb):
        UniqueDict = {}
        for item in listOb:
            UniqueDict[item] = 0
        return UniqueDict

    ######################################################################
    # Function: GetRols
    #
    # Description:
    #    Get the rols.
    #
    # Parameters:
    #    DiceTypelist  - the Combo list tuple.
    #    function      - the function.
    #
    # Return: 
    #    DataDict - the probabilities Dict of the selected funcation.
    ######################################################################
    def GetRols(self, DiceTypelist, function):
        FinelList = self.__DiceCombination(DiceTypelist)
        DataDict = self.__FuncRole(FinelList, function)
        total = sum(DataDict.values())
        for key in DataDict.keys():
            DataDict[key] = round(DataDict[key]/total * 100, 2)

        return DataDict


