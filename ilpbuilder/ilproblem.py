def coeff_sum(coeff_map):
    res=""
    is_first=True
    for var_name, coeff  in coeff_map.items():
        if is_first: 
          sign="-" if coeff<0 else ""
          is_first=False
        else:
          sign="- " if coeff<0 else "+ "
          
        res+=sign+str(abs(coeff))+" "+str(var_name)+" "
        
    return res

class ILCostFunction:
     #constants:
    MIN="min"
    MAX="max"
    COST_KIND= {MIN :'min',
                MAX :'max'}
                
    def __init__(self, KIND="min"):
        self.pref = ILCostFunction.COST_KIND[KIND]
        self.cost_fun=None
        
    def set_coeff_map(self, coeff_map):
        self.cost_fun=dict(coeff_map) 
        
    def toString(self):
        if self.cost_fun is None:
            return self.pref+":"
        else:
            return self.pref+": "+coeff_sum(self.cost_fun)+";" 
    
    
    def isMin(self):
        return self.pref==ILCostFunction.COST_KIND[ILCostFunction.MIN]
    
    def isMax(self):
        return self.pref==ILCostFunction.COST_KIND[ILCostFunction.MAX]
        
    def getObjectiveAsString(self):
        if self.cost_fun is None:
            return "0"
        else:
            return coeff_sum(self.cost_fun)
    
class ILConstrain:
    #constants:
    LESS="LESS"
    LESS_EQUAL="LESS_EQUAL"
    EQUAL="EQUAL"
    GREATER_EQUAL="GREATER_EQUAL"
    GREATER="GREATER"
    OPS=       {LESS :'<',
               LESS_EQUAL :'<=',
               EQUAL :'=',
               GREATER_EQUAL:'>=',
               GREATER:'>'}
               
    def __init__(self,  OP, result=None, name=None):
        self.op=ILConstrain.OPS[OP]
        self.result=result
        self.name=name      
        self.coeff_map={}
    
    def add_coeff(self, var_id, value):
        self.coeff_map[var_id]=value
    
    def set_result(self, new_result):
        self.result=new_result
       
    def set_name(self, new_name):
        self.name=new_name
    
    def set_operation(self, OP):
        self.op=ILConstrain.OPS[OP]
        
    def toString(self):
        """returns the constrain assuming coeff_keys are the names of the variables"""
        
        if not self.coeff_map:
            raise Exception('no coeffs in constrain %s'%self.name)
            
        if self.result is None:
            raise Exception('result of this constrain is unknown!')
                       
        if self.name is None:
            res=""
        else:
            res=self.name+": "
            
        res+=coeff_sum(self.coeff_map) 
            
        res+=self.op
        res+=" "+str(self.result)
        
        return res; 
        
        
class ILProblem:
    
    def __init__(self, cost_fun_kind='min'):
        self.comment="model created by ilpbuilder"
        self.constrains=[]
        self.bin_vars=set()
        self.int_vars=set()
        self.free_vars=set()
        self.cost_fun=ILCostFunction(cost_fun_kind)
    
    def add_constrain(self, constrain):
        self.constrains.append(constrain)
        
    def append_constrains(self, constrains):
        self.constrains.extend(constrains)
        
    def set_cost_fun(self,coeff_map):
        self.cost_fun.set_coeff_map(coeff_map)
        
    def define_as_bin_vars(self, var_names):
        self.bin_vars.update(var_names)
    
    def define_as_int_vars(self,var_names):
        self.int_vars.update(var_names)
    
    def export(self, exporter):
        res=[];
        
        #header:
        exporter.comment_found(self.comment)
        exporter.empty_line_found()
         
        #cost fun:
        exporter.cost_fun_found(self.cost_fun)      
        exporter.empty_line_found()
        
        #constrains:
        for constrain in self.constrains:
            exporter.constrain_found(constrain)
        exporter.empty_line_found()
        
        #definitions:
        #bin:
        exporter.bin_vars_found(self.bin_vars)
               
        #int: 
        exporter.int_vars_found(self.int_vars)

